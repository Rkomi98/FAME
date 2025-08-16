"""
Database setup script for FAME application.
This script can be used to initialize the database with tables.
"""

import os
from app import create_app
from models import db

def setup_database():
    """Create all database tables."""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Print some info
        print(f"📊 Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print(f"🔧 Environment: {os.environ.get('FLASK_ENV', 'development')}")

if __name__ == "__main__":
    setup_database()
