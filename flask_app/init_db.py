import sys
import os

# Ensure the root directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_app.run_app import app
from flask_app.auth.models import User, database

# Debug: confirm which DB is being used
print("Using database at:", app.config['SQLALCHEMY_DATABASE_URI'])

with app.app_context():
    # Drop all tables if they exist
    database.drop_all()
    database.create_all()
    print("Database was created successfully.")

    # Optional: Seed a default admin user
    from werkzeug.security import generate_password_hash

    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password_hash=generate_password_hash('admin123'), role='admin')
        database.session.add(admin)
        database.session.commit()
        print("Default admin user created (username: admin, password: admin123)")
