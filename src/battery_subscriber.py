"""This module handles all the requests to battery subscriber service."""

import logging

from flask import Blueprint, request, jsonify

from src.database.database import db
from src.database.model_battery import Battery


logger = logging.getLogger()

battery_subscriber = Blueprint(
    "battery_subscriber", __name__, url_prefix="/api/v1/subscriber/"
)


@battery_subscriber.route("/batteries", methods=["GET"])
def get_all_batteries():
    """Retrieve a list of all batteries and their associated data."""

    batteries = Battery.query.all()
    battery_list = []
    for battery in batteries:
        battery_list.append(
            {
                "id": str(battery.id),
                "state_of_charge": battery.state_of_charge,
                "capacity": battery.capacity,
                "voltage": battery.voltage,
                "battery_health": battery.battery_health,
                "created_at": battery.created_at,
                "updated_at": battery.updated_at,
            }
        )
    return jsonify(battery_list)


@battery_subscriber.route("/batteries/<uuid:id>", methods=["GET"])
def get_battery_by_id(id):
    """Retrieve the data for a specific battery by its ID."""

    battery = Battery.query.get(id)
    if battery:
        return jsonify(
            {
                "id": str(battery.id),
                "state_of_charge": battery.state_of_charge,
                "capacity": battery.capacity,
                "voltage": battery.voltage,
                "battery_health": battery.battery_health,
                "created_at": battery.created_at,
                "updated_at": battery.updated_at,
            }
        )
    else:
        return jsonify({"message": "Battery not found"}), 404


@battery_subscriber.route("/batteries", methods=["POST"])
def add_battery():
    """Add a new battery with its state of charge, capacity, and voltage."""

    data = request.json
    state_of_charge = data.get("state_of_charge")
    capacity = data.get("capacity")
    voltage = data.get("voltage")
    battery_health = data.get("battery_health")

    battery = Battery(state_of_charge, capacity, voltage, battery_health)
    db.session.add(battery)
    db.session.commit()

    return jsonify({"message": "Battery added successfully"}), 201


@battery_subscriber.route("/batteries/<uuid:id>", methods=["PUT"])
def update_battery(id):
    """Update the data for a specific battery by its ID."""

    battery = Battery.query.get(id)
    if battery:
        data = request.json
        battery.state_of_charge = data.get("state_of_charge")
        battery.capacity = data.get("capacity")
        battery.voltage = data.get("voltage")
        battery.battery_health = data.get("battery_health")
        db.session.commit()
        return jsonify({"message": "Battery updated successfully"})
    else:
        return jsonify({"message": "Battery not found"}), 404


@battery_subscriber.route("/batteries/<uuid:id>", methods=["DELETE"])
def delete_battery(id):
    """Remove a specific battery by its ID."""

    battery = Battery.query.get(id)
    if battery:
        db.session.delete(battery)
        db.session.commit()
        return jsonify({"message": "Battery deleted successfully"})
    else:
        return jsonify({"message": "Battery not found"}), 404
