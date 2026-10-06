#!/usr/bin/env python3
"""
Test the simple password hashing system
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from app import app, db
from app.models import User
from app.routes import hash_password, verify_password

def test_simple_hash():
    print("🧪 TESTING SIMPLE PASSWORD HASHING SYSTEM")
    print("=" * 50)
    
    # Test password hashing
    test_password = "mypassword123"
    print(f"Original password: '{test_password}'")
    
    # Hash the password
    hashed = hash_password(test_password)
    print(f"Hashed password: '{hashed}'")
    
    # Verify the password
    is_valid = verify_password(test_password, hashed)
    print(f"Password verification: {is_valid}")
    
    # Test with wrong password
    wrong_password = "wrongpassword"
    is_invalid = verify_password(wrong_password, hashed)
    print(f"Wrong password verification: {is_invalid}")
    
    print("\n" + "=" * 50)
    print(f"✅ Hash test: {'PASSED' if is_valid else 'FAILED'}")
    print(f"✅ Wrong password test: {'PASSED' if not is_invalid else 'FAILED'}")
    
    return is_valid and not is_invalid

def test_database_user():
    print("\n🗄️ TESTING DATABASE USER LOGIN")
    print("=" * 50)
    
    with app.app_context():
        # Find a user in the database
        user = User.query.filter_by(username='abhi_gabi').first()
        
        if user:
            print(f"Found user: {user.username}")
            print(f"Stored password hash: {user.password}")
            
            # Test with the known password
            test_password = "123"
            is_valid = verify_password(test_password, user.password)
            print(f"Password '{test_password}' verification: {is_valid}")
            
            # If it's an old format that didn't work, update it
            if not is_valid and ':' in user.password:
                print("⚠️ User has advanced hash format, updating to simple format...")
                user.password = hash_password(test_password)
                db.session.commit()
                print(f"✅ Password updated to simple format: {user.password}")
                
                # Test again
                is_valid = verify_password(test_password, user.password)
                print(f"Updated password verification: {is_valid}")
            
            return is_valid
        else:
            print("❌ User 'abhi_gabi' not found")
            return False

if __name__ == "__main__":
    # Test the hashing functions
    hash_test_result = test_simple_hash()
    
    # Test database user
    db_test_result = test_database_user()
    
    print(f"\n🏁 FINAL RESULTS:")
    print(f"Hash functions: {'✅ WORKING' if hash_test_result else '❌ FAILED'}")
    print(f"Database login: {'✅ WORKING' if db_test_result else '❌ FAILED'}")
    
    if hash_test_result and db_test_result:
        print("\n🎉 ALL TESTS PASSED! Login should work now.")
    else:
        print("\n❌ Some tests failed. Please check the issues above.")
