from datetime import datetime
from ..extensions import db
import json

class ActivityLog(db.Model):
    __tablename__ = "activity_log"
    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, nullable=True)  # user who triggered
    action = db.Column(db.String(256))
    data = db.Column(db.Text)  # JSON text
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def as_dict(self):
        try:
            payload = json.loads(self.data) if self.data else {}
        except Exception:
            payload = {"raw": self.data}
        return {
            "id": self.id,
            "actor_id": self.actor_id,
            "action": self.action,
            "data": payload,
            "created_at": self.created_at.isoformat()
        }
