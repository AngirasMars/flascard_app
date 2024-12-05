from app import db, User, app

# Delete the old admin user (if any) and create a new one
with app.app_context():
    admin_user = User.query.filter_by(id='admin').first()

    if admin_user:
        db.session.delete(admin_user)
        db.session.commit()
    
    # Create a new admin user
    new_admin_user = User(id='admin', password='adminpassword', role='admin')
    db.session.add(new_admin_user)
    db.session.commit()

    print("Old admin user deleted and new one added successfully")
