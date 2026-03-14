"""
WSGI entry point for production deployment
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create and configure Flask app
from app import create_app, db

app = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == "__main__":
    app.run()
