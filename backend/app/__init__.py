from flask import Flask
from .config import Config
from .extensions import db, migrate, redis_client
from .routes import register_routes

def create_app(config_object=None):
    app = Flask(__name__, static_folder=None)
    app.config.from_object(config_object or Config)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # create DB and seed admin if needed
    with app.app_context():
        from .seeds.create_admin import ensure_admin
        db.create_all()
        ensure_admin()

    # register routes blueprint
    register_routes(app)
    return app
