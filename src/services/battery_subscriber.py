"""This module handles all the requests to battery subscriber service."""

import logging

from flask import Blueprint, request, jsonify

from src.database.database import db
from src.database.model_battery import Battery
from src.utils.input_validators import validate_input


logger = logging.getLogger()

battery_subscriber = Blueprint(
    "battery_subscriber", __name__, url_prefix="/api/v1/subscriber/"
)


@battery_subscriber.get("/batteries")
def get_all_batteries():
    """Retrieve a list of all batteries and their associated data."""

    batteries = Battery.query.all()
    battery_list = []
    for battery in batteries:
        battery_list.append(
            {
                "id": str(battery.battery_id),
                "state_of_charge": battery.state_of_charge,
                "capacity": battery.capacity,
                "voltage": battery.voltage,
                "battery_health": battery.battery_health,
                "created_at": battery.created_at,
                "updated_at": battery.updated_at,
            }
        )
    return jsonify(battery_list)


@battery_subscriber.get("/batteries/<uuid:battery_id>")
def get_battery_by_id(battery_id):
    """Retrieve the data for a specific battery by its ID."""

    battery = Battery.query.get(battery_id)
    if battery:
        return jsonify(
            {
                "id": str(battery.battery_id),
                "state_of_charge": battery.state_of_charge,
                "capacity": battery.capacity,
                "voltage": battery.voltage,
                "battery_health": battery.battery_health,
                "created_at": battery.created_at,
                "updated_at": battery.updated_at,
            }
        )
    return jsonify({"message": "Battery not found"}), 404


@battery_subscriber.post("/batteries")
@validate_input(api="subscriber")
def add_battery():
    """Add a new battery with its state of charge, capacity, and voltage."""

    data = request.json
    state_of_charge = data.get("state_of_charge")
    capacity = data.get("capacity")
    voltage = data.get("voltage")
    battery_health = data.get("battery_health")

    battery = Battery(state_of_charge, capacity, voltage, battery_health)
    battery_id = battery.battery_id
    db.session.add(battery)
    db.session.commit()
    db.session.close()

    return (
        jsonify(
            {
                "message": "Battery added successfully!",
                "battery_id": battery_id,
            }
        ),
        201,
    )


@battery_subscriber.put("/batteries/<uuid:battery_id>")
@validate_input(api="subscriber")
def update_battery(battery_id):
    """Updates battery's status of charge, health, and voltage."""

    battery = Battery.query.get(battery_id)
    if battery:
        data = request.json
        battery.update_battery(
            state_of_charge=data.get("state_of_charge"),
            voltage=data.get("voltage"),
            battery_health=data.get("battery_health"),
        )
        return jsonify(
            {"message": "Battery updated successfully", "id": battery_id}
        )
    return jsonify({"message": f"Battery '{battery_id}' not found"}), 404


@battery_subscriber.delete("/batteries/<uuid:battery_id>")
def delete_battery(battery_id):
    """Remove a specific battery by its ID."""

    battery = Battery.query.get(battery_id)
    if battery:
        db.session.delete(battery)
        db.session.commit()
        db.session.close()

        return jsonify({"message": "Battery deleted successfully"})
    return jsonify({"message": "Battery not found"}), 404
