"""This module contains database model for Batteries."""

import uuid
from datetime import datetime, timedelta

from src.database.database import db
from src.config.app_config import BATTERY_HEALTH_ORDER


class Battery(db.Model):
    """DB ORM for 'Batteries' table."""

    __tablename__ = "batteries"

    battery_id = db.Column(db.String, primary_key=True)
    state_of_charge = db.Column(db.Float)
    capacity = db.Column(db.Float)
    voltage = db.Column(db.Float)
    battery_health = db.Column(
        db.Enum(BATTERY_HEALTH_ORDER), default="EXCELLENT"
    )
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
        self.battery_id = battery_id if battery_id else str(uuid.uuid4())
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

    def calculate_health(self):
        """Checks the historical health check on the battery
        and updates its status if needed."""

        # Get the state of charge values for the last 24 hours
        yesterday = datetime.utcnow() - timedelta(days=1)
        state_of_charge_values = (
            db.session.query(Battery.state_of_charge)
            .filter(Battery.id == self.id, Battery.updated_at >= yesterday)
            .all()
        )

        # Count the number of times the state of charge exceeds the limits
        exceed_count = 0
        for value in state_of_charge_values:
            if value.state_of_charge < 20 or value.state_of_charge > 80:
                exceed_count += 1

        # Update the health based on the exceed count
        if self.battery_health != "BAD" and exceed_count > 2:
            index = BATTERY_HEALTH_ORDER.index(self.battery_health)
            self.battery_health = BATTERY_HEALTH_ORDER[index - 1]

    def update_battery(
        self, state_of_charge, capacity, voltage, battery_health
    ):
        """Updates battery's record in the database."""

        self.state_of_charge = state_of_charge
        self.capacity = capacity
        self.voltage = voltage
        self.battery_health = battery_health
        self.calculate_health()
        db.session.commit()
        db.session.close()
