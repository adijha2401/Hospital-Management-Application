from flask import Blueprint, request, jsonify, session
from ..utils.auth import login_required, doctor_required
from ..extensions import db
from ..models.appointment import Appointment
from ..models.treatment import Treatment
from ..models.doctor import Doctor
from ..models.patient import Patient
from datetime import datetime

doctor_bp = Blueprint("doctor", __name__)

@doctor_bp.route("/dashboard", methods=["GET"])
@login_required
@doctor_required
def dashboard():
    user_id = session.get("user_id")
    # list upcoming appointments for this doctor
    appts = Appointment.query.filter_by(doctor_id=user_id).filter(Appointment.status=="Booked").order_by(Appointment.start_dt).all()
    return jsonify({"upcoming": [a.as_dict() for a in appts]})

@doctor_bp.route("/appointment/<int:appt_id>/status", methods=["PUT"])
@login_required
@doctor_required
def update_status(appt_id):
    data = request.get_json() or {}
    status = data.get("status")
    if status not in ("Completed", "Cancelled", "Booked"):
        return jsonify({"error": "invalid status"}), 400
    appt = Appointment.query.get_or_404(appt_id)
    appt.status = status
    db.session.commit()
    return jsonify({"message": "status_updated", "appointment": appt.as_dict()})

@doctor_bp.route("/appointment/<int:appt_id>/treatment", methods=["POST"])
@login_required
@doctor_required
def add_treatment(appt_id):
    data = request.get_json() or {}
    diagnosis = data.get("diagnosis")
    prescription = data.get("prescription")
    notes = data.get("notes")
    # verify appointment exists
    appt = Appointment.query.get_or_404(appt_id)
    t = Treatment(appointment_id=appt.id, diagnosis=diagnosis, prescription=prescription, notes=notes)
    appt.status = "Completed"
    db.session.add(t)
    db.session.commit()
    return jsonify({"message": "treatment_saved", "treatment": t.as_dict()})

@doctor_bp.route("/patients", methods=["GET"])
@login_required
@doctor_required
def list_patients():
    user_id = session.get("user_id")
    # all patients who had appointments with this doctor
    appts = Appointment.query.filter_by(doctor_id=user_id).all()
    patient_ids = {a.patient_id for a in appts}
    patients = Patient.query.filter(Patient.id.in_(patient_ids)).all()
    return jsonify({"patients": [p.as_dict() for p in patients]})
