"""This module checks the health condition for a battery."""

from datetime import datetime, timedelta

from src.database.database import db
from src.database.model_battery_log import BatteryLog

from src.config.app_config import BATTERY_HEALTH_ORDER


class HealthCheck:
    """Checks the battery's state of health."""

    def __init__(self, battery_id, current_health, request_time):
        self.battery_id = battery_id
        self.request_time = request_time
        self.current_health = current_health

    def check_condition(self):
        """Checks the state of charge for the battery and returns a state of health."""

        # Get the state of charge values for the last 24 hours
        yesterday = datetime.utcnow() - timedelta(days=1)
        state_of_charge_values = (
            db.session.query(BatteryLog.state_of_charge)
            .filter(
                BatteryLog.battery_id == self.battery_id,
                BatteryLog.timestamp >= yesterday,
            )
            .all()
        )

        # Count the number of times the state of charge exceeds the limits
        exceed_count = 0
        for value in state_of_charge_values:
            if value.state_of_charge < 20 or value.state_of_charge > 80:
                exceed_count += 1

        # Update the health based on the exceed count
        if self.current_health != "BAD" and exceed_count > 2:
            index = BATTERY_HEALTH_ORDER.index(self.current_health)
            self.current_health = BATTERY_HEALTH_ORDER[index - 1]

        return self.current_health
