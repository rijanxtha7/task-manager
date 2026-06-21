import os
from flask import Flask
import config

def create_app():
    """Flask app factory"""
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY
    
    # Initialize database tables on startup
    with app.app_context():
        from app.database import create_tables
        create_tables()
    
    return app