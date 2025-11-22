from functools import wraps
from flask import session, jsonify

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return jsonify({"error": "authentication required"}), 401
        return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if session.get("role") != "admin":
            return jsonify({"error": "admin role required"}), 403
        return fn(*args, **kwargs)
    return wrapper

def doctor_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if session.get("role") != "doctor":
            return jsonify({"error": "doctor role required"}), 403
        return fn(*args, **kwargs)
    return wrapper

def patient_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if session.get("role") != "patient":
            return jsonify({"error": "patient role required"}), 403
        return fn(*args, **kwargs)
    return wrapper
