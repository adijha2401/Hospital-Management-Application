# Import models for alembic/flask-migrate convenience
from .user import User
from .department import Department
from .doctor import Doctor
from .patient import Patient
from .appointment import Appointment
from .treatment import Treatment
from .activity_log import ActivityLog
# Export SQLAlchemy db for direct import convenience
from ..extensions import db
