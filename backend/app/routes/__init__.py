from flask import Blueprint
from flask import jsonify

def register_routes(app):
    from .auth_routes import auth_bp
    from .admin_routes import admin_bp
    from .doctor_routes import doctor_bp
    from .patient_routes import patient_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(doctor_bp, url_prefix="/api/doctor")
    app.register_blueprint(patient_bp, url_prefix="/api/patient")

    @app.route("/api/health")
    def health():
        return jsonify({"status": "ok"}), 200
