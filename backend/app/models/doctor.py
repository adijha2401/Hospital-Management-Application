from datetime import datetime
from ..extensions import db

class Doctor(db.Model):
    __tablename__ = "doctor"
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User', backref='doctor_profile', uselist=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)
    specialization = db.Column(db.String(128))
    # availability stored as JSON string (simple approach)
    availability = db.Column(db.Text)  # JSON: list of available slot datetimes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def as_dict(self):
        return {
            "id": self.id,
            "username": self.user.username if self.user else None,
            "email": self.user.email if self.user else None,
            "specialization": self.specialization,
            "department_id": self.department_id,
            "availability": self.availability
        }
