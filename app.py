import logging
import json


from flask import Flask, request, Response
from flask_cors import CORS

from src.database.database import db
from src.config import app_config
from src.config.logs import LOG_CONFIG

from src.battery_subscriber import battery_subscriber
from src.battery_incidents import battery_incidents


logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)


app = Flask(__name__)


app.config.from_mapping(
    SECRET_KEY=app_config.SECRET_KEY,
    SQLALCHEMY_DATABASE_URI=app_config.DB_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)


CORS(app, resources={r"/api/*": {"origins": "*"}})

db.app = app
db.init_app(app)

# Blueprints: start #
app.register_blueprint(battery_subscriber)
app.register_blueprint(battery_incidents)
# Blueprints: end #
