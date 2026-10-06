"""
Script to add Payment table to the database
Run this script after updating the models.py file
"""

from app import app, db
from app.models import User, Product, VerifiedSeller, Payment

with app.app_context():
    try:
        # Create the Payment table
        db.create_all()
        print("✅ Payment table created successfully!")
        print("Database schema updated.")
        
        # Verify the table was created
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        if 'payment' in tables:
            print("✅ Payment table exists in database")
            columns = [col['name'] for col in inspector.get_columns('payment')]
            print(f"Columns: {', '.join(columns)}")
        else:
            print("❌ Payment table not found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
