"""This module contains database model for Battery Issues."""

import uuid
from datetime import datetime

from src.database.database import db


class Issue(db.Model):
    """DB ORM for 'Issues' table."""

    __tablename__ = "incidents"

    issue_id = db.Column(
        db.String, primary_key=True
    )  # SQLLite does not have a native UUID type.
    issue_type = db.Column(db.String(50))
    issue_description = db.Column(db.String(255))
    occurrence_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, issue_type, issue_description, issue_id=None):
        self.issue_id = issue_id if issue_id else str(uuid.uuid4())
        self.issue_type = issue_type
        self.issue_description = issue_description

    def __repr__(self):
        return (
            f"Issue("
            f"id={self.issue_id}, "
            f"type='{self.issue_type}', "
            f"timestamp='{self.occurrence_timestamp}'"
            f")"
        )
