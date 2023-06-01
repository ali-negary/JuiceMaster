"""This method contains unittests for Battery Health Check service."""

import os
import unittest
from datetime import datetime
from unittest.mock import patch

from src.database.model_battery_log import BatteryLog
from src.services.battery_health_check import HealthCheck
from src.app import create_app


class HealthCheckTestCase(unittest.TestCase):
    """Test cases for Battery Health Check service."""

    def setUp(self):
        """Set up the test data."""

        self.battery_id = "battery-123"
        self.voltage = 1
        self.current_health = "EXCELLENT"
        self.request_time = datetime.utcnow()

        # Create a Flask app with the test configuration
        os.environ["TEST_MODE"] = "True"
        os.environ["SQLALCHEMY_DB_URI"] = "sqlite:///:memory:"
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Clean up the test data and the Flask app context."""
        self.app_context.pop()

    @patch("src.database.database.db.session.query")
    def test_check_condition_health_unchanged(self, mock_query):
        # Create a mock query object
        mock_filter = mock_query.return_value.filter

        # Set up the mock filter to return specific values
        mock_filter.return_value.all.return_value = [
            BatteryLog(
                battery_id=self.battery_id,
                voltage=self.voltage,
                state_of_charge=30,
            ),
            BatteryLog(
                battery_id=self.battery_id,
                voltage=self.voltage,
                state_of_charge=40,
            ),
            BatteryLog(
                battery_id=self.battery_id,
                voltage=self.voltage,
                state_of_charge=50,
            ),
        ]

        # Create an instance of HealthCheck
        health_check = HealthCheck(
            self.battery_id, self.current_health, self.request_time
        )

        # Call the check_condition method
        result = health_check.check_condition()

        # Assert the expected result
        self.assertEqual(result, "EXCELLENT")

    @patch("src.database.database.db.session.query")
    def test_check_condition_health_updated(self, mock_filter):
        """Test that the health is updated if state of charge values exceed limits."""
        # Create a mock query object
        mock_filter = mock_filter.return_value.filter

        # Set up the mock filter to return specific values
        mock_filter.return_value.all.return_value = [
            BatteryLog(
                battery_id=self.battery_id,
                voltage=self.voltage,
                state_of_charge=10,
            ),
            BatteryLog(
                battery_id=self.battery_id,
                voltage=self.voltage,
                state_of_charge=40,
            ),
            BatteryLog(
                battery_id=self.battery_id,
                voltage=self.voltage,
                state_of_charge=90,
            ),
        ]
        # Create an instance of HealthCheck
        health_check = HealthCheck(
            self.battery_id, self.current_health, self.request_time
        )

        # Call the check_condition method
        result = health_check.check_condition()

        # Assert that the health is updated
        self.assertNotEqual(result, "VERY GOOD")
