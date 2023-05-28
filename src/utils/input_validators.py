"""This module contains the input validator for batteries and issues APIs."""

import functools

from flask import request, jsonify

from src.config.app_config import BATTERY_HEALTH_ORDER


def validate_battery_data(data):
    """Performs validation checks on the battery data.
    Returns an error message if the data is not valid."""

    state_of_charge = data.get("state_of_charge")
    if state_of_charge:
        if not isinstance(state_of_charge, (int, float)):
            return "Invalid 'type' for state of charge"
        if not (0 < state_of_charge < 100):
            return f"Charge value '{state_of_charge}' is not in the valid range (0-100)."

    capacity = data.get("capacity")
    if capacity:
        if not isinstance(capacity, (int, float)):
            return "Invalid 'type' for capacity"

    voltage = data.get("voltage")
    if voltage:
        if not isinstance(voltage, (int, float)):
            return "Invalid 'type' for voltage"

    battery_health = data.get("battery_health")
    if battery_health:
        if not isinstance(battery_health, str):
            return "Invalid 'type' for battery health"
        if battery_health not in BATTERY_HEALTH_ORDER:
            return "Invalid 'value' for battery health"

    return None


def validate_issue_data(data):
    """Performs validation checks on the issue data.
    Returns an error message if the data is not valid."""

    if not isinstance(data.get("issue_type"), str):
        return "Invalid 'type' for issue"

    if not isinstance(data.get("issue_description"), str):
        return "Invalid issue description"

    return None


def validate_input(api):
    def decorator(func):
        """Performs validation checks on input data.
        Returns {"error": "error message"} if invalid."""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json()

            if api == "subscriber":
                error = validate_battery_data(data=data)
            elif api == "incidents":
                error = validate_issue_data(data=data)
            else:
                raise ValueError("Invalid API specified.")

            if error:
                return jsonify({"error": error}), 400
            return func(*args, **kwargs)

        return wrapper

    return decorator