import os

"""Flask configuration."""

class Config:
    """Base config"""
    TESTING = True
    DEBUG = True
    FLASK_ENV = 'development'
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

    