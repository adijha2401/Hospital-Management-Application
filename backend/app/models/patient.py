from datetime import datetime
from ..extensions import db

class Patient(db.Model):
    __tablename__ = "patient"
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User', backref='patient_profile', uselist=False)
    contact = db.Column(db.String(64))
    dob = db.Column(db.Date, nullable=True)
    extra_info = db.Column(db.Text)  # JSON or free-text medical notes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def as_dict(self):
        return {
            "id": self.id,
            "username": self.user.username if self.user else None,
            "email": self.user.email if self.user else None,
            "contact": self.contact,
            "dob": self.dob.isoformat() if self.dob else None
        }
