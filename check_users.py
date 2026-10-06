#!/usr/bin/env python3
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from app.models import User

def check_users():
    with app.app_context():
        users = User.query.all()
        print(f"Found {len(users)} users in database:")
        for user in users:
            print(f"  - Username: {user.username}")
            print(f"  - Password Hash (first 50 chars): {user.password[:50]}...")
            print(f"  - Hash Format: {'Advanced' if ':' in user.password and user.password.count(':') >= 2 else 'Old/Fallback' if '$' in user.password else 'Unknown'}")
            print()

if __name__ == "__main__":
    check_users()
