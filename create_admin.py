"""
Script to create an admin user in the database.
Run this script to create an admin account: python create_admin.py
"""

from app import app, db
from app.models import User
import hashlib
import secrets

def hash_password(password):
    """Hash a password with a random salt using SHA-256"""
    salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}${password_hash}"

def create_admin():
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(username='admin').first()
        
        if admin:
            print("⚠️  Admin user already exists!")
            update = input("Do you want to update the admin password? (yes/no): ")
            if update.lower() != 'yes':
                print("❌ Operation cancelled.")
                return
            
            # Update password
            new_password = input("Enter new admin password: ")
            admin.password = hash_password(new_password)
            admin.role = 'admin'
            db.session.commit()
            print("✅ Admin password updated successfully!")
        else:
            # Create new admin user
            print("Creating new admin user...")
            username = input("Enter admin username (default: admin): ").strip() or 'admin'
            password = input("Enter admin password: ")
            
            if not password:
                print("❌ Password cannot be empty!")
                return
            
            new_admin = User(
                username=username,
                password=hash_password(password),
                role='admin'
            )
            
            db.session.add(new_admin)
            db.session.commit()
            print(f"✅ Admin user '{username}' created successfully!")
            print(f"   Role: admin")

if __name__ == '__main__':
    print("=" * 50)
    print("Admin User Creation Script")
    print("=" * 50)
    create_admin()
    print("=" * 50)
