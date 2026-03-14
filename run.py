#!/usr/bin/env python
"""
X - Twitter Clone
Main entry point for the Flask application
"""

import os
from app import create_app, db
from app.models import User, LoginSession, PasswordReset, LoginRequest

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Create Flask app
app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Register shell context for flask shell"""
    return {
        'db': db,
        'User': User,
        'LoginSession': LoginSession,
        'PasswordReset': PasswordReset,
        'LoginRequest': LoginRequest
    }

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return '''
    <div style="text-align: center; padding: 50px;">
        <h1>404 - Page Not Found</h1>
        <p>The page you're looking for doesn't exist.</p>
        <a href="/" style="color: #1d9bf0;">Go Home</a>
    </div>
    ''', 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return '''
    <div style="text-align: center; padding: 50px;">
        <h1>500 - Server Error</h1>
        <p>Something went wrong. Please try again later.</p>
        <a href="/" style="color: #1d9bf0;">Go Home</a>
    </div>
    ''', 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') == 'development')
