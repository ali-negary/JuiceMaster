"""This is the main module that integrates all the services."""

import os
import logging

from flask import Flask
from flask_cors import CORS

from src.database.database import db
from src.config.logs import LOG_CONFIG

from src.services.battery_subscriber import battery_subscriber
from src.services.battery_issues import battery_issues


logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)


def create_app():
    # Application configuration: start #
    secret_key = os.environ.get("SECRET_KEY", "Juice-Master-Secret-Key")
    db_uri = os.environ.get("SQLALCHEMY_DB_URI")
    test_mode = True if os.environ.get("TEST_MODE", False) == "True" else False

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=secret_key,
        SQLALCHEMY_DATABASE_URI=db_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        TESTING=test_mode,
    )
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.app = app
    db.init_app(app)
    # Application configuration: end #

    # Blueprints: start #
    app.register_blueprint(battery_subscriber)
    app.register_blueprint(battery_issues)
    # Blueprints: end #

    return app


if __name__ == "__main__":
    create_app()
