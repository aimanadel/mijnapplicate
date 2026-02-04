"""Entry point for Flask application"""

from flask import Flask

from app.events import bp as events_bp
from app.main import bp as main_bp


def create_app():
    app = Flask(__name__)
    app.config["FLASK_ADMIN_FLUID_LAYOUT"] = True
    app.config["SECRET_KEY"] = "DokkiePythoniAXRvULKWuFyfURRrG0YTOOTXswLJWpU"

    app.config.from_pyfile("settings.py")

    app.register_blueprint(main_bp)

    app.register_blueprint(events_bp, url_prefix="/events")

    return app
