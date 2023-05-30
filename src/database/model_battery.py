"""This module contains database model for Batteries."""

import uuid
from datetime import datetime

from src.database.database import db


class Battery(db.Model):
    """DB ORM for 'Batteries' table."""

    __tablename__ = "batteries"

    battery_id = db.Column(
        db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    state_of_charge = db.Column(db.Float)
    capacity = db.Column(db.Integer)
    voltage = db.Column(db.Float)
    battery_health = db.Column(db.String, default="EXCELLENT")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(
        self,
        state_of_charge,
        capacity,
        voltage,
        battery_health,
        battery_id=None,
    ):
        self.battery_id = battery_id if battery_id else uuid.uuid4()
        self.state_of_charge = state_of_charge
        self.capacity = capacity
        self.voltage = voltage
        self.battery_health = battery_health

    def __repr__(self) -> str:
        return (
            f"Battery("
            f"id='{self.battery_id}', "
            f"charge={self.state_of_charge}%, "
            f"health='{self.battery_health}', "
            f"updated_at='{self.updated_at}'"
            f")"
        )


# DDL QUERY: start #

# CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
# CREATE TYPE battery_health_enum AS ENUM ('BAD', 'GOOD', 'VERY GOOD', 'EXCELLENT');
#
# CREATE TABLE batteries (
#     battery_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
#     state_of_charge FLOAT,
#     capacity INTEGER,
#     voltage FLOAT,
#     battery_health battery_health_enum DEFAULT 'EXCELLENT',
#     created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
# );

# DDL QUERY: end #
