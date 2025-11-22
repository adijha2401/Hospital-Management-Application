from flask import Blueprint, request, jsonify, session
from ..extensions import db
from ..models.user import User
from ..models.doctor import Doctor
from ..models.department import Department
from ..models.appointment import Appointment
from ..utils.auth import login_required, admin_required
from sqlalchemy import func

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/dashboard", methods=["GET"])
@login_required
@admin_required
def dashboard():
    total_doctors = User.query.filter_by(role="doctor").count()
    total_patients = User.query.filter_by(role="patient").count()
    total_appointments = Appointment.query.count()
    return jsonify({
        "doctors": total_doctors,
        "patients": total_patients,
        "appointments": total_appointments
    })

@admin_bp.route("/doctor", methods=["POST"])
@login_required
@admin_required
def add_doctor():
    data = request.get_json() or {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password", "Doctor@123")
    specialization = data.get("specialization")
    department_id = data.get("department_id")

    if not username or not email:
        return jsonify({"error": "username and email required"}), 400
    if User.query.filter((User.username==username) | (User.email==email)).first():
        return jsonify({"error": "user already exists"}), 400

    u = User(username=username, email=email, role="doctor")
    u.set_password(password)
    db.session.add(u)
    db.session.flush()  # get id

    d = Doctor(id=u.id, specialization=specialization, department_id=department_id)
    db.session.add(d)
    db.session.commit()
    return jsonify({"message": "doctor_added", "doctor": d.as_dict()}), 201

@admin_bp.route("/doctor/<int:doctor_id>", methods=["PUT"])
@login_required
@admin_required
def edit_doctor(doctor_id):
    data = request.get_json() or {}
    d = Doctor.query.get_or_404(doctor_id)
    specialization = data.get("specialization")
    dept = data.get("department_id")
    if specialization:
        d.specialization = specialization
    if dept is not None:
        d.department_id = dept
    db.session.commit()
    return jsonify({"message": "updated", "doctor": d.as_dict()})

@admin_bp.route("/doctor/<int:doctor_id>", methods=["DELETE"])
@login_required
@admin_required
def delete_doctor(doctor_id):
    # soft-delete approach: remove user entry or mark blacklisted by changing role
    doc_user = User.query.get_or_404(doctor_id)
    doc_user.role = "blacklisted"
    db.session.commit()
    return jsonify({"message": "doctor_blacklisted"})

@admin_bp.route("/appointments", methods=["GET"])
@login_required
@admin_required
def list_appointments():
    # optional query params: status, date_from, date_to
    args = request.args
    q = Appointment.query
    status = args.get("status")
    if status:
        q = q.filter_by(status=status)
    # TODO: add date filtering
    appts = q.order_by(Appointment.start_dt.desc()).limit(200).all()
    return jsonify({"appointments": [a.as_dict() for a in appts]})

@admin_bp.route("/search", methods=["GET"])
@login_required
@admin_required
def search():
    typ = request.args.get("type", "doctor")
    q = request.args.get("q", "")
    if typ == "doctor":
        doctors = User.query.filter(User.role=="doctor").filter(func.lower(User.username).contains(q.lower())).limit(50).all()
        return jsonify({"doctors": [u.as_dict() for u in doctors]})
    elif typ == "patient":
        patients = User.query.filter(User.role=="patient").filter(func.lower(User.username).contains(q.lower())).limit(50).all()
        return jsonify({"patients": [u.as_dict() for u in patients]})
    else:
        return jsonify({"error": "unknown type"}), 400
