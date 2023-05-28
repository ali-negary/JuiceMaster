"""This module contains application configurations."""


import os



SECRET_KEY = os.environ.get("SECRET_KEY", "Juice-Master-Secret-Key")
DB_URI = os.environ.get("SQLALCHEMY_DB_URI")


BATTERY_HEALTH_ORDER = ('BAD', 'GOOD', 'VERY GOOD', 'EXCELLENT')
