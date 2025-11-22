from flask import Blueprint, request, jsonify, session
from ..utils.auth import login_required, patient_required
from ..extensions import db, redis_client
from ..models.department import Department
from ..models.doctor import Doctor
from ..models.appointment import Appointment
from ..models.patient import Patient
from datetime import datetime
from sqlalchemy.exc import IntegrityError

patient_bp = Blueprint("patient", __name__)

@patient_bp.route("/departments", methods=["GET"])
@login_required
@patient_required
def departments():
    key = "departments:all"
    cached = redis_client.get(key)
    if cached:
        import json
        return jsonify({"departments": json.loads(cached)})
    depts = Department.query.all()
    out = [d.as_dict() for d in depts]
    import json
    redis_client.set(key, json.dumps(out), ex=300)
    return jsonify({"departments": out})

@patient_bp.route("/doctors", methods=["GET"])
@login_required
@patient_required
def search_doctors():
    specialization = request.args.get("specialization")
    q = Doctor.query
    if specialization:
        q = q.filter(Doctor.specialization.ilike(f"%{specialization}%"))
    docs = q.limit(100).all()
    return jsonify({"doctors": [d.as_dict() for d in docs]})

@patient_bp.route("/doctor/<int:doctor_id>/availability", methods=["GET"])
@login_required
@patient_required
def doctor_availability(doctor_id):
    d = Doctor.query.get_or_404(doctor_id)
    # If availability cached in redis, return cached value
    key = f"doctor:{doctor_id}:availability"
    cached = redis_client.get(key)
    if cached:
        import json
        return jsonify({"availability": json.loads(cached)})
    # fallback: parse availability JSON field (may be None)
    import json
    try:
        avail = json.loads(d.availability) if d.availability else []
    except Exception:
        avail = []
    redis_client.set(key, json.dumps(avail), ex=60)
    return jsonify({"availability": avail})

@patient_bp.route("/appointment", methods=["POST"])
@login_required
@patient_required
def book_appointment():
    data = request.get_json() or {}
    patient_id = session.get("user_id")
    doctor_id = data.get("doctor_id")
    start_dt = data.get("start_dt")  # ISO string
    end_dt = data.get("end_dt")
    if not (doctor_id and start_dt and end_dt):
        return jsonify({"error": "doctor_id, start_dt and end_dt required"}), 400
    try:
        from dateutil import parser
        start_dt_parsed = parser.isoparse(start_dt)
        end_dt_parsed = parser.isoparse(end_dt)
    except Exception:
        return jsonify({"error": "invalid datetime format; use ISO format"}), 400

    appt = Appointment(patient_id=patient_id, doctor_id=doctor_id,
                       start_dt=start_dt_parsed, end_dt=end_dt_parsed)
    try:
        db.session.add(appt)
        db.session.commit()
        return jsonify({"message": "appointment_booked", "appointment": appt.as_dict()}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "slot already taken for this doctor"}), 409

@patient_bp.route("/appointment/<int:appt_id>", methods=["PUT"])
@login_required
@patient_required
def reschedule(appt_id):
    # allow patient to reschedule their own appointment if it's booked
    data = request.get_json() or {}
    user_id = session.get("user_id")
    appt = Appointment.query.get_or_404(appt_id)
    if appt.patient_id != user_id:
        return jsonify({"error": "not allowed"}), 403
    if appt.status != "Booked":
        return jsonify({"error": "only booked appointments can be rescheduled"}), 400
    start_dt = data.get("start_dt")
    end_dt = data.get("end_dt")
    if not (start_dt and end_dt):
        return jsonify({"error": "start_dt and end_dt required"}), 400
    try:
        from dateutil import parser
        start_dt_parsed = parser.isoparse(start_dt)
        end_dt_parsed = parser.isoparse(end_dt)
    except Exception:
        return jsonify({"error": "invalid datetime format"}), 400
    appt.start_dt = start_dt_parsed
    appt.end_dt = end_dt_parsed
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "conflict or invalid update"}), 409
    return jsonify({"message": "rescheduled", "appointment": appt.as_dict()})

@patient_bp.route("/appointment/<int:appt_id>", methods=["DELETE"])
@login_required
@patient_required
def cancel(appt_id):
    user_id = session.get("user_id")
    appt = Appointment.query.get_or_404(appt_id)
    if appt.patient_id != user_id:
        return jsonify({"error": "not allowed"}), 403
    appt.status = "Cancelled"
    db.session.commit()
    return jsonify({"message": "cancelled"})

@patient_bp.route("/history", methods=["GET"])
@login_required
@patient_required
def history():
    user_id = session.get("user_id")
    appts = Appointment.query.filter_by(patient_id=user_id).order_by(Appointment.start_dt.desc()).all()
    return jsonify({"appointments": [a.as_dict() for a in appts]})

@patient_bp.route("/export_csv", methods=["POST"])
@login_required
@patient_required
def export_csv():
    """
    Enqueue CSV export job. We will return a job token.
    The Celery worker will generate CSV and send notification (email or store on disk).
    """
    from ...tasks.export_csv import export_patient_treatments_csv
    user_id = session.get("user_id")
    email = request.json.get("email") or None
    job = export_patient_treatments_csv.delay(user_id, email)
    return jsonify({"message": "export_started", "job_id": job.id}), 202
