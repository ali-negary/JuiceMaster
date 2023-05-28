"""This method contains unittests for Battery Issues API."""

import os
import unittest

from src.app import create_app
from src.database.database import db
from src.database.model_battery import Battery
from src.database.model_incident import Issue


class IssueAPITestCase(unittest.TestCase):
    """Test case for the Issue API."""

    def setUp(self):
        """Set up the test environment."""

        # Create a test Flask app
        os.environ["TEST_MODE"] = "True"
        os.environ["SQLALCHEMY_DB_URI"] = "sqlite:///:memory:"
        app = create_app()
        self.app = app
        self.client = app.test_client()

        # Initialize the test database
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Tear down the test environment."""

        # Clean up the test database
        with self.app.app_context():
            db.drop_all()

    def test_add_issue(self):
        """Test adding an issue to a battery."""

        # Add a battery to the database
        with self.app.app_context():
            battery = Battery(
                battery_id=1,
                state_of_charge=50,
                capacity=100,
                voltage=12,
                battery_health="EXCELLENT",
            )
            db.session.add(battery)
            db.session.commit()

        # Make a POST request to add an issue to the battery
        response = self.client.post(
            "/api/v1/incidents/batteries/1/issues",
            json={
                "issue_type": "temperature warning",
                "issue_description": "High temperature",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_get_issues(self):
        """Test retrieving issues of a battery."""

        # Add a battery and an issue to the database
        with self.app.app_context():
            battery = Battery(
                battery_id=1,
                state_of_charge=50,
                capacity=100,
                voltage=12,
                battery_health="EXCELLENT",
            )
            issue = Issue(
                issue_id=1,
                issue_type="temperature warning",
                issue_description="High temperature",
            )
            db.session.add(battery)
            db.session.add(issue)
            db.session.commit()

        # Make a GET request to retrieve the issues of the battery
        response = self.client.get("/api/v1/incidents/batteries/1/issues")
        self.assertEqual(response.status_code, 200)

    def test_update_issue(self):
        """Test updating an issue."""

        # Add a battery and an issue to the database
        with self.app.app_context():
            battery = Battery(
                battery_id=1,
                state_of_charge=50,
                capacity=100,
                voltage=12,
                battery_health="EXCELLENT",
            )
            issue = Issue(
                issue_id=1,
                issue_type="temperature warning",
                issue_description="High temperature",
            )
            db.session.add(battery)
            db.session.add(issue)
            db.session.commit()

        # Make a PUT request to update the issue
        response = self.client.put(
            "/api/v1/incidents/batteries/1/issues/1",
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
            battery = Battery(
                battery_id=1,
                state_of_charge=50,
                capacity=100,
                voltage=12,
                battery_health="EXCELLENT",
            )
            issue = Issue(
                issue_id=1,
                issue_type="temperature warning",
                issue_description="High temperature",
            )
            db.session.add(battery)
            db.session.add(issue)
            db.session.commit()

        # Make a DELETE request to remove the issue
        response = self.client.delete("/api/v1/incidents/batteries/1/issues/1")
        self.assertEqual(response.status_code, 200)
