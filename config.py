import os
from datetime import timedelta


class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Database Configuration - Support both SQLite and PostgreSQL
    uri = os.environ.get("DATABASE_URL")

    if uri and uri.startswith("postgres://"):
        # Force SQLAlchemy to use pg8000
        uri = uri.replace("postgres://", "postgresql+pg8000://", 1)

    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session Configuration
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # News API configuration
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY') or 'demo'
    NEWS_REFRESH_INTERVAL = 3600  # Refresh news every hour

    # Flask-Login configuration
    REMEMBER_COOKIE_DURATION = timedelta(days=7)

    # Production settings
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    FLASK_DEBUG = FLASK_ENV != 'production'
