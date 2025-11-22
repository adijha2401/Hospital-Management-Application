from .celery_app import celery
from ..app import create_app
from ..extensions import db
from ..models.appointment import Appointment
from datetime import date
from ..utils.notifications import send_email, send_gchat

app = create_app()

@celery.task(name="tasks.daily_reminder.send_daily_reminders")
def send_daily_reminders():
    """
    Find appointments scheduled today and send reminders via email / chat.
    """
    with app.app_context():
        today = date.today()
        appts = Appointment.query.filter(db.func.date(Appointment.start_dt) == today, Appointment.status == "Booked").all()
        for a in appts:
            # lazy load patient email
            try:
                patient_email = a.patient.user.email
            except Exception:
                patient_email = None
            subject = "Appointment Reminder"
            body = f"Dear patient, this is a reminder for your appointment at {a.start_dt}."
            if patient_email:
                send_email(subject, body, patient_email)
            # optional: GChat or SMS integration could be used here
    return True
