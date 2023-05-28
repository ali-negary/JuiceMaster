"""This module handles all the requests to battery incidents service."""

import logging

from flask import Blueprint, request, jsonify

from src.database.database import db
from src.database.model_incident import Issue
from src.database.model_battery import Battery
from src.utils.input_validators import validate_input

logger = logging.getLogger()

battery_issues = Blueprint(
    "battery_issues", __name__, url_prefix="/api/v1/issues/"
)


@battery_issues.get("/batteries/<uuid:id>/issues")
@validate_input(api="incidents")
def get_battery_issues(id):
    """Retrieve a list of all issues associated with a specific battery."""

    battery = Battery.query.get(id)
    if battery:
        issues = battery.issues
        issue_list = []
        for issue in issues:
            issue_list.append(
                {
                    "id": issue.id,
                    "issue_type": issue.issue_type,
                    "issue_description": issue.issue_description,
                    "occurrence_timestamp": issue.occurrence_timestamp,
                }
            )
        return jsonify(issue_list)
    else:
        return jsonify({"message": "Battery not found"}), 404


@battery_issues.post("/batteries/<uuid:id>/issues")
@validate_input(api="incidents")
def add_battery_issue(id):
    """Add a new issue associated with a specific battery."""

    battery = Battery.query.get(id)
    if battery:
        data = request.json
        issue_type = data.get("issue_type")
        issue_description = data.get("issue_description")

        issue = Issue(issue_type, issue_description)
        battery.issues.append(issue)
        db.session.commit()
        db.session.close()

        return jsonify({"message": "Issue added successfully"}), 201
    else:
        return jsonify({"message": "Battery not found"}), 404


@battery_issues.put("/batteries/<uuid:battery_id>/issues/<int:issue_id>")
@validate_input(api="incidents")
def update_battery_issue(battery_id, issue_id):
    """Update the details of a specific issue associated with a battery."""

    battery = Battery.query.get(battery_id)
    if battery:
        issue = Issue.query.get(issue_id)
        if issue:
            data = request.json
            issue.issue_type = data.get("issue_type")
            issue.issue_description = data.get("issue_description")
            db.session.commit()
            db.session.close()

            return jsonify({"message": "Issue updated successfully"})
        else:
            return jsonify({"message": "Issue not found"}), 404
    else:
        return jsonify({"message": "Battery not found"}), 404


@battery_issues.delete("/batteries/<uuid:battery_id>/issues/<int:issue_id>")
@validate_input(api="incidents")
def delete_battery_issue(battery_id, issue_id):
    """Remove a specific issue associated with a battery."""

    battery = Battery.query.get(battery_id)
    if battery:
        issue = Issue.query.get(issue_id)
        if issue:
            battery.issues.remove(issue)
            db.session.commit()
            db.session.close()

            return jsonify({"message": "Issue deleted successfully"})
        else:
            return jsonify({"message": "Issue not found"}), 404
    else:
        return jsonify({"message": "Battery not found"}), 404