from datetime import datetime
from ..extensions import db

class Appointment(db.Model):
    __tablename__ = "appointment"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    start_dt = db.Column(db.DateTime, nullable=False)
    end_dt = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(32), default="Booked")  # Booked / Completed / Cancelled
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('doctor_id', 'start_dt', name='uix_doctor_start'),
    )

    def as_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "start_dt": self.start_dt.isoformat(),
            "end_dt": self.end_dt.isoformat(),
            "status": self.status
        }
