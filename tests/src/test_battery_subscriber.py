"""This method contains unittests for Battery Subscriber API."""

import os
import unittest
import uuid

from src.app import create_app
from src.database.database import db
from src.database.model_battery import Battery


class BatteryAPITestCase(unittest.TestCase):
    """Test case for the Subscriber API."""

    def setUp(self):
        """Set up the test environment."""

        # Create a test Flask app
        os.environ["TEST_MODE"] = "True"
        os.environ[
            "SQLALCHEMY_DB_URI"
        ] = "postgresql://username:password@localhost:5432/database"
        app = create_app()
        self.app = app
        self.client = app.test_client()

        # Initialize the test database
        with self.app.app_context():
            db.create_all()

        self.battery_id = uuid.uuid4()

    def tearDown(self):
        """Tear down the test environment."""

        # Clean up the test database
        with self.app.app_context():
            db.drop_all()

    def test_add_battery(self):
        """Test adding a battery."""

        response = self.client.post(
            "/api/v1/batteries",
            json={
                "state_of_charge": 50,
                "capacity": 100,
                "voltage": 12,
                "battery_health": "EXCELLENT",
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_get_all_batteries(self):
        """Test retrieving all battery records."""

        # Add a battery to the database
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
            db.session.close()

        # Make a GET request to retrieve the battery
        response = self.client.get("/api/v1/batteries")
        self.assertEqual(response.status_code, 200)

    def test_get_battery(self):
        """Test retrieving a specific battery."""

        # Add a battery to the database
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
            db.session.close()

        # Make a GET request to retrieve the battery
        response = self.client.get(f"/api/v1/batteries/{self.battery_id}")
        self.assertEqual(response.status_code, 200)

    def test_update_battery(self):
        """Test updating a battery."""

        # Add a battery to the database
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
            db.session.close()

        # Make a PUT request to update the battery
        response = self.client.put(
            f"/api/v1/batteries/{self.battery_id}",
            json={
                "state_of_charge": 70,
                "capacity": 120,
                "voltage": 12.5,
                "battery_health": "GOOD",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_battery(self):
        """Test deleting a battery."""

        # Add a battery to the database
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
            db.session.close()

        # Make a DELETE request to remove the battery
        response = self.client.delete(f"/api/v1/batteries/{self.battery_id}")
        self.assertEqual(response.status_code, 200)
