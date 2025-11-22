from celery import Celery
from ..app.config import Config

celery = Celery(
    "hms_tasks",
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND
)

# Import task modules so celery discovers tasks
# (relative import will be resolved when this module is imported)
# Celery beat schedule is configured below or can be managed externally
celery.conf.beat_schedule = {
    "daily_reminder_morning": {
        "task": "tasks.daily_reminder.send_daily_reminders",
        # every day at 08:30 (cron)
        "schedule": {"type": "crontab", "hour": 8, "minute": 30}
    },
    "monthly_report_first": {
        "task": "tasks.monthly_report.send_monthly_reports",
        "schedule": {"type": "crontab", "day_of_month": "1", "hour": 6, "minute": 0}
    }
}
