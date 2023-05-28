"""This module contains database model for Battery Incidents."""

from datetime import datetime
import uuid

from sqlalchemy.dialects.postgresql import UUID

from src.database.database import db


class Incident(db.Model):

    __tablename__ = 'incidents'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    issue_type = db.Column(db.String(50))
    issue_description = db.Column(db.String(255))
    occurrence_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, issue_type, issue_description):
        self.issue_type = issue_type
        self.issue_description = issue_description

    def __repr__(self):
        return f"Incident(" \
               f"id={self.id}, " \
               f"type='{self.issue_type}', " \
               f"timestamp='{self.occurrence_timestamp}'" \
               f")"
