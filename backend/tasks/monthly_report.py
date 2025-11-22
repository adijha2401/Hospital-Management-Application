from .celery_app import celery
from ..app import create_app
from ..extensions import db
from ..models import Appointment, Treatment, Doctor, User
from datetime import date, timedelta
from ..utils.notifications import send_email
import os

app = create_app()

@celery.task(name="tasks.monthly_report.send_monthly_reports")
def send_monthly_reports():
    """
    For each doctor, generate a simple HTML/monthly summary and email to the doctor's email.
    This is a simple implementation. You may enhance it to create PDFs or detailed HTML.
    """
    with app.app_context():
        # determine last month period (previous calendar month)
        today = date.today()
        first_of_this_month = today.replace(day=1)
        last_month_end = first_of_this_month - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1)

        doctors = User.query.filter_by(role="doctor").all()
        for doc in doctors:
            # gather appointments for this doctor in the last month
            appts = Appointment.query.filter(
                Appointment.doctor_id == doc.id,
                db.func.date(Appointment.start_dt) >= last_month_start,
                db.func.date(Appointment.start_dt) <= last_month_end
            ).all()
            total = len(appts)
            # sample HTML
            html = f"<h1>Monthly Report for Dr. {doc.username}</h1>"
            html += f"<p>Period: {last_month_start} to {last_month_end}</p>"
            html += f"<p>Total appointments: {total}</p>"
            for a in appts:
                t = a.treatment if hasattr(a, "treatment") else None
                html += f"<div><strong>Appointment:</strong> {a.start_dt} - Status: {a.status}</div>"
                if t:
                    html += f"<div>Diagnosis: {t.diagnosis}</div>"
            # send email to doctor
            if doc.email:
                try:
                    send_email(f"Monthly Report - {last_month_start} to {last_month_end}", html, doc.email)
                except Exception as e:
                    print("Failed to send report to", doc.email, e)
    return True
