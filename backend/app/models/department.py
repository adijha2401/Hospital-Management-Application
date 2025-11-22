from datetime import datetime
from ..extensions import db

class Department(db.Model):
    __tablename__ = "department"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def as_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description}
