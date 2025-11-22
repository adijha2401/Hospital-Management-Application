from flask import Blueprint, request, jsonify, session, current_app
from ..extensions import db
from ..models.user import User
from ..models.patient import Patient
from ..models.doctor import Doctor
from werkzeug.security import generate_password_hash
from datetime import datetime

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register_patient():
    """
    Patient registration endpoint.
    Request JSON: { username, email, password, contact (optional) }
    """
    data = request.get_json() or {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    contact = data.get("contact")

    if not all([username, email, password]):
        return jsonify({"error": "username, email, password required"}), 400

    if User.query.filter((User.username==username) | (User.email==email)).first():
        return jsonify({"error": "user with username/email already exists"}), 400

    u = User(username=username, email=email, role="patient")
    u.set_password(password)
    db.session.add(u)
    db.session.commit()

    p = Patient(id=u.id, contact=contact)
    db.session.add(p)
    db.session.commit()

    return jsonify({"message": "registered", "user": u.as_dict()}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    identifier = data.get("identifier")  # username or email
    password = data.get("password")
    if not identifier or not password:
        return jsonify({"error": "identifier and password required"}), 400

    user = User.query.filter((User.username==identifier) | (User.email==identifier)).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "invalid credentials"}), 401

    # Basic session-based auth for simplicity. Frontend stores session cookie.
    session['user_id'] = user.id
    session['role'] = user.role
    session.permanent = True

    return jsonify({"message": "logged_in", "user": user.as_dict()}), 200

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "logged_out"}), 200
