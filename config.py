import os
from datetime import timedelta


class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///news_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # News API configuration
    NEWS_API_KEY = os.environ.get(
        'NEWS_API_KEY') or 'demo'  # Get from newsapi.org
    NEWS_REFRESH_INTERVAL = 3600  # Refresh news every hour (in seconds)

    # Flask-Login configuration
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
