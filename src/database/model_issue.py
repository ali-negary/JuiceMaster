"""This module contains database model for Battery Issues."""

import uuid
from datetime import datetime

from src.database.database import db


class Issue(db.Model):
    """DB ORM for 'Issues' table."""

    __tablename__ = "issues"

    issue_id = db.Column(
        db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    battery_id = db.Column(db.UUID, db.ForeignKey("batteries.battery_id"))
    issue_type = db.Column(db.String(50))
    issue_description = db.Column(db.String(255))
    occurrence_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    battery = db.relationship("Battery", backref="issues")

    def __init__(self, issue_type, issue_description, issue_id=None):
        self.issue_id = issue_id if issue_id else uuid.uuid4()
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


# DDL QUERY: start #

# CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
#
# CREATE TABLE issues (
#     issue_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
#     battery_id UUID REFERENCES batteries(battery_id),
#     issue_type VARCHAR(50),
#     issue_description VARCHAR(255),
#     occurrence_timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
# );

# DDL QUERY: end #
