"""This method contains unittests for Battery Issues API."""

import os
import unittest
import uuid

from src.app import create_app
from src.database.database import db
from src.database.model_battery import Battery
from src.database.model_issue import Issue


class IssueAPITestCase(unittest.TestCase):
    """Test case for the Issue API."""

    def setUp(self):
        """Set up the test environment."""

        # Create a test Flask app
        os.environ["TEST_MODE"] = "True"
        os.environ[
            "SQLALCHEMY_DB_URI"
        ] = "postgresql://username:password@localhost:5432/database"
        self.app = create_app()
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

        self.battery_id = uuid.uuid4()
        self.issue_id = uuid.uuid4()

        with self.app.app_context():
            battery = Battery(
                battery_id=self.battery_id,
                state_of_charge=50,
                capacity=100,
                voltage=12,
                battery_health="EXCELLENT",
            )
            db.session.add(battery)
            db.session.commit()

    def tearDown(self):
        """Tear down the test environment."""

        # Clean up the test database
        with self.app.app_context():
            db.drop_all()

    def test_add_issue(self):
        """Test adding an issue to a battery."""

        # Make a POST request to add an issue to the battery
        response = self.client.post(
            f"/api/v1/batteries/{self.battery_id}/issues",
            json={
                "issue_type": "temperature warning",
                "issue_description": "High temperature",
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_get_issues(self):
        """Test retrieving issues of a battery."""

        # Add a battery and an issue to the database
        with self.app.app_context():
            issue = Issue(
                issue_id=self.issue_id,
                issue_type="temperature warning",
                issue_description="High temperature",
                battery_id=self.battery_id,
            )
            db.session.add(issue)
            db.session.commit()

        # Make a GET request to retrieve the issues of the battery
        response = self.client.get(
            f"/api/v1/batteries/{self.battery_id}/issues"
        )
        self.assertEqual(response.status_code, 200)

    def test_update_issue(self):
        """Test updating an issue."""

        # Add a battery and an issue to the database
        with self.app.app_context():
            issue = Issue(
                issue_id=self.issue_id,
                issue_type="temperature warning",
                issue_description="High temperature",
                battery_id=self.battery_id,
            )
            db.session.add(issue)
            db.session.commit()

        # Make a PUT request to update the issue
        response = self.client.put(
            f"/api/v1/batteries/{self.battery_id}/issues/{self.issue_id}",
            json={
                "issue_type": "overcharge alert",
                "issue_description": "Battery overcharged",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_issue(self):
        """Test deleting an issue."""

        # Add a battery and an issue to the database
        with self.app.app_context():
            issue = Issue(
                issue_id=self.issue_id,
                issue_type="temperature warning",
                issue_description="High temperature",
                battery_id=self.battery_id,
            )
            db.session.add(issue)
            db.session.commit()

        # Make a DELETE request to remove the issue
        response = self.client.delete(
            f"/api/v1/batteries/{self.battery_id}/issues/{self.issue_id}"
        )
        self.assertEqual(response.status_code, 200)
