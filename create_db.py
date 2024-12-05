from app import db, app  # Import db and app from app.py

# Create the application context
with app.app_context():
    db.create_all()  # Create tables in the database
    print("Database created successfully.")
