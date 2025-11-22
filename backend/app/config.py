import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "very-secret-key-for-dev")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, '..', 'hms.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis (for caching / celery broker config references)
    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

    # Celery settings (app-level convenience)
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", REDIS_URL)
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", REDIS_URL)

    # Session config (optional)
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
