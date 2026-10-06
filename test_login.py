#!/usr/bin/env python3
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from app.routes import verify_password

def test_password_verification():
    """Test password verification for different hash formats"""
    
    # Test cases based on actual database data
    test_cases = [
        # Plain text passwords (legacy)
        ("admin", "admin", "Expected: True (plain text)"),
        ("srinu", "srinu", "Expected: True (plain text)"),
        ("wrong", "admin", "Expected: False (wrong password)"),
        
        # Old hash format (salt$hash)
        ("Akhilesh_password", "9193ce41f6184f0a2052e1110fe339a6$374faa89b66552060", "Expected: True if correct (old hash)"),
        ("wrong_password", "9193ce41f6184f0a2052e1110fe339a6$374faa89b66552060", "Expected: False (wrong password)"),
        
        # New advanced format would need actual password to test
    ]
    
    print("Testing password verification function:")
    print("=" * 50)
    
    for i, (password, stored_hash, description) in enumerate(test_cases, 1):
        try:
            result = verify_password(password, stored_hash)
            print(f"Test {i}: {description}")
            print(f"  Password: '{password}'")
            print(f"  Hash: '{stored_hash[:50]}...'")
            print(f"  Result: {result}")
            print()
        except Exception as e:
            print(f"Test {i}: ERROR - {e}")
            print()

if __name__ == "__main__":
    test_password_verification()
