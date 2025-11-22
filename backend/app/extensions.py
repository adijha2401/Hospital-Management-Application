from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import redis
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

# lazy redis client; app context not required for simple usage
redis_client = redis.Redis.from_url(Config.REDIS_URL, decode_responses=True)
