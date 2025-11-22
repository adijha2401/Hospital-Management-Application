import json
from flask import current_app
from ..extensions import redis_client

def cache_set(key, value, ex=300):
    try:
        redis_client.set(key, json.dumps(value), ex=ex)
    except Exception:
        current_app.logger.warning("Redis set failed for key %s", key)

def cache_get(key):
    try:
        v = redis_client.get(key)
        if v:
            return json.loads(v)
    except Exception:
        pass
    return None
