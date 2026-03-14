from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
import os
from datetime import timedelta

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()

def create_app(config_name=None):
    """Application factory function"""
    app = Flask(__name__)
    
    # Configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    if config_name == 'production':
        from config import ProductionConfig
        app.config.from_object(ProductionConfig)
    elif config_name == 'testing':
        from config import TestingConfig
        app.config.from_object(TestingConfig)
    else:
        from config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    
    # Login manager setup
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    login_manager.session_protection = 'strong'
    app.permanent_session_lifetime = timedelta(days=7)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from app.routes import auth_bp, account_bp, security_bp, main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(account_bp)
    app.register_blueprint(security_bp)
    app.register_blueprint(main_bp)
    
    return app
