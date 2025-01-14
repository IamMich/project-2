# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///events.db'  # Ensure this is correct for SQLite or another database
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Optional: Disable tracking modifications to avoid overhead
    SECRET_KEY = os.urandom(24)  # Set a secret key for sessions
