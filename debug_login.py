#!/usr/bin/env python3
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from app.models import User
from app.routes import verify_password, hash_password

def test_actual_user_login():
    """Test login with actual users from database"""
    
    with app.app_context():
        print("Testing actual user login processes:")
        print("=" * 50)
        
        # Test each user in the database
        users = User.query.all()
        
        for user in users:
            print(f"\n👤 Testing user: {user.username}")
            print(f"   Password hash: {user.password}")
            print(f"   Hash format: {'Advanced' if ':' in user.password and user.password.count(':') >= 2 else 'Old/Fallback' if '$' in user.password else 'Plain Text'}")
            
            # For plain text users, test with their username as password
            if not '$' in user.password and not ':' in user.password:
                print(f"   Testing plain text password: '{user.username}'")
                result = verify_password(user.username, user.password)
                print(f"   ✅ Result: {result}")
                
                if result:
                    print(f"   🔄 Testing hash generation for migration...")
                    new_hash = hash_password(user.username)
                    print(f"   📝 New hash would be: {new_hash[:50]}...")
            else:
                print(f"   ⚠️  Cannot test - need original password for hashed users")
            
            print("-" * 30)

def test_login_flow():
    """Test the complete login flow"""
    print("\n🔐 TESTING COMPLETE LOGIN FLOW")
    print("=" * 50)
    
    # Test case: admin user with plain text password
    username = "admin"
    password = "admin"
    
    print(f"Testing login: {username}/{password}")
    
    with app.app_context():
        # Step 1: Find user
        user = User.query.filter_by(username=username).first()
        if not user:
            print("❌ User not found")
            return
        
        print(f"✅ User found: {user.username}")
        print(f"   Stored password: {user.password}")
        
        # Step 2: Verify password
        print(f"🔍 Verifying password...")
        try:
            result = verify_password(password, user.password)
            print(f"   Verification result: {result}")
            
            if result:
                print("✅ Login would succeed!")
                
                # Step 3: Check if migration needed
                needs_migration = ':' not in user.password or user.password.count(':') < 2
                print(f"   Migration needed: {needs_migration}")
                
                if needs_migration:
                    print("🔄 Testing password migration...")
                    new_hash = hash_password(password)
                    print(f"   New hash: {new_hash[:50]}...")
                    
            else:
                print("❌ Login would fail!")
                
        except Exception as e:
            print(f"❌ Error during verification: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_actual_user_login()
    test_login_flow()
