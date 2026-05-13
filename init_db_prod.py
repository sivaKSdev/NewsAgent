import os
from app import app, db

# Load production environment
from dotenv import load_dotenv
load_dotenv('.env.production.local')

with app.app_context():
    db.create_all()
    print("✓ Database initialized successfully!")
