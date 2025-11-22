import smtplib
from email.message import EmailMessage
import os
import requests

def send_email(subject, body, to_email, from_email=None):
    # Simple SMTP using environment variables (dev). For production, use a proper mail service.
    SMTP_HOST = os.environ.get("SMTP_HOST")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
    SMTP_USER = os.environ.get("SMTP_USER")
    SMTP_PASS = os.environ.get("SMTP_PASS")
    FROM = from_email or SMTP_USER or "noreply@example.com"
    if not SMTP_HOST:
        # fallback: log to console
        print("EMAIL (simulated):", subject, "->", to_email)
        return True

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = FROM
    msg["To"] = to_email
    msg.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.starttls()
        if SMTP_USER and SMTP_PASS:
            s.login(SMTP_USER, SMTP_PASS)
        s.send_message(msg)
    return True

def send_gchat(webhook_url, message):
    """
    Send a simple text message to Google Chat webhook
    """
    if not webhook_url:
        print("GChat webhook not provided. Message:", message)
        return False
    payload = {"text": message}
    try:
        r = requests.post(webhook_url, json=payload, timeout=5)
        return r.status_code == 200
    except Exception as e:
        print("Failed to send gchat:", e)
        return False
