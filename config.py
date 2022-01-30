"""Flask configuration."""

class Config:
    """Base config"""
    TESTING = True
    DEBUG = True
    FLASK_ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

    