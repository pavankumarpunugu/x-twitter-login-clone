import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_REFRESH_EACH_REQUEST = True
    
    # CSRF
    WTF_CSRF_TIME_LIMIT = None
    WTF_CSRF_SSL_STRICT = True
    
    # Mail
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@x-twitter-clone.com')
    
    # Security
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION = 30  # minutes
    PASSWORD_RESET_TIMEOUT = 24  # hours
    EMAIL_CONFIRMATION_TIMEOUT = 24  # hours


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///app.db'
    )
    SESSION_COOKIE_SECURE = False
    WTF_CSRF_SSL_STRICT = False
    MAIL_DEBUG = True


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    MAIL_BACKEND = 'locmem'
    SESSION_COOKIE_SECURE = False
    WTF_CSRF_SSL_STRICT = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
    # Ensure all required settings are set
    assert SECRET_KEY != 'dev-secret-key-change-in-production', "SECRET_KEY must be set in production"
    assert SQLALCHEMY_DATABASE_URI, "DATABASE_URL must be set in production"
    
    # Security
    SESSION_COOKIE_SECURE = True
    WTF_CSRF_SSL_STRICT = True
    PREFERRED_URL_SCHEME = 'https'
