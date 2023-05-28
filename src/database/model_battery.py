"""This module contains database model for Batteries."""

import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID

from src.database.database import db


class Battery(db.Model):

    __tablename__ = 'batteries'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    state_of_charge = db.Column(db.Float)
    capacity = db.Column(db.Float)
    voltage = db.Column(db.Float)
    battery_health = db.Column(db.Enum('BAD', 'GOOD', 'VERY GOOD', 'EXCELLENT'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, state_of_charge, capacity, voltage, battery_health):
        self.state_of_charge = state_of_charge
        self.capacity = capacity
        self.voltage = voltage
        self.battery_health = battery_health

    def __repr__(self) -> str:
        return f"Battery(" \
               f"id='{self.id}', " \
               f"charge={self.state_of_charge}%, " \
               f"health='{self.battery_health}', " \
               f"updated_at='{self.updated_at}'" \
               f")"
