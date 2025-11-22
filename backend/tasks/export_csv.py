from .celery_app import celery
from ..app import create_app
from ..extensions import db
from ..models.appointment import Appointment
from ..models.treatment import Treatment
from ..models.user import User
import csv
import os
from ..utils.notifications import send_email

app = create_app()
EXPORT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "exports"))
os.makedirs(EXPORT_DIR, exist_ok=True)

@celery.task(name="tasks.export_csv.export_patient_treatments_csv")
def export_patient_treatments_csv(patient_id, notify_email=None):
    """
    Generate a CSV with patient's treatments and appointments; save to exports/ and optionally email.
    """
    with app.app_context():
        filename = f"patient_{patient_id}_treatments.csv"
        filepath = os.path.join(EXPORT_DIR, filename)

        appts = Appointment.query.filter_by(patient_id=patient_id).order_by(Appointment.start_dt).all()
        headers = ["user_id", "username", "doctor_id", "appointment_date", "status", "diagnosis", "prescription", "notes"]

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for a in appts:
                username = a.patient.user.username if hasattr(a, "patient") and a.patient and a.patient.user else ""
                doctor_id = a.doctor_id
                appt_date = a.start_dt.isoformat()
                status = a.status
                # attempt to find treatment
                t = Treatment.query.filter_by(appointment_id=a.id).first()
                diagnosis = t.diagnosis if t else ""
                prescription = t.prescription if t else ""
                notes = t.notes if t else ""
                writer.writerow([patient_id, username, doctor_id, appt_date, status, diagnosis, prescription, notes])

        # optionally email the CSV
        if notify_email:
            try:
                send_email("Your treatment export", f"Please find attached CSV: {filename}", notify_email)
                # attaching files to plain send_email requires enhancement; here we just notify
            except Exception as e:
                print("Failed to notify by email:", e)
        return {"filepath": filepath}
