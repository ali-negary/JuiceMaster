"""This module contains database model for Battery Logs."""

from datetime import datetime

from src.database.database import db


class BatteryLog(db.Model):
    """DB ORM for 'battery_logs' table."""

    __tablename__ = "battery_logs"

    battery_id = db.Column(db.UUID, primary_key=True)
    state_of_charge = db.Column(db.Float)
    voltage = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, battery_id, state_of_charge, voltage, timestamp=None):
        self.battery_id = battery_id
        self.state_of_charge = state_of_charge
        self.voltage = voltage
        self.timestamp = timestamp


# DDL QUERY: start #

# CREATE TABLE battery_logs (
#     battery_id UUID,
#     state_of_charge FLOAT,
#     voltage FLOAT,
#     timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
# );

# DDL QUERY: end #
