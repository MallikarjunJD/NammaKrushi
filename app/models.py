
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")


# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(20), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tasks', lazy=True))

# Inventory model
class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('inventory', lazy=True))

# Expense model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    season = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('expenses', lazy=True))

# Journal model for farming activities
class Journal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(50), nullable=False)  # Planting, Watering, Fertilizing, Pest Control, Harvesting, Soil Preparation
    activity_details = db.Column(db.Text, nullable=False)  # Description of the activity
    date = db.Column(db.String(20), nullable=False)  # Date of the activity
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('journal_entries', lazy=True))

# Product model for marketplace
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # vegetables, fruits, grains, dairy, organic
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.String(50), nullable=False)
    unit = db.Column(db.String(20), nullable=False)  # kg, g, L, units, bags
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(200), nullable=True)
    contact = db.Column(db.String(50), nullable=True)
    date_posted = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, active, sold, rejected
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('products', lazy=True))

# Verified Seller model
class VerifiedSeller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    verified_farming_seller = db.Column(db.Boolean, nullable=False, default=False)
    verification_status = db.Column(db.String(20), nullable=False, default='not_requested')  # not_requested, pending, approved, rejected
    
    # Farmer details for verification
    farm_name = db.Column(db.String(200), nullable=True)
    farm_location = db.Column(db.String(200), nullable=True)
    farm_size = db.Column(db.String(50), nullable=True)  # in acres/hectares
    farming_experience = db.Column(db.String(50), nullable=True)  # in years
    crops_grown = db.Column(db.Text, nullable=True)  # comma-separated list
    phone_number = db.Column(db.String(20), nullable=True)
    id_proof_number = db.Column(db.String(100), nullable=True)  # Aadhar/PAN/License
    
    # Admin response
    rejection_reason = db.Column(db.Text, nullable=True)
    verified_date = db.Column(db.String(20), nullable=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('seller_verification', uselist=False, lazy=True))

# Payment Logs model
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(100), unique=True, nullable=False)
    
    # Order details
    order_items = db.Column(db.Text, nullable=False)  # JSON string of cart items
    total_amount = db.Column(db.Float, nullable=False)
    
    # Delivery address
    full_name = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address_line1 = db.Column(db.String(500), nullable=False)
    address_line2 = db.Column(db.String(500), nullable=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    
    # Payment details
    payment_screenshot = db.Column(db.Text, nullable=False)  # Base64 encoded image
    payment_date = db.Column(db.String(20), nullable=False)
    
    # Admin verification
    payment_status = db.Column(db.String(20), nullable=False, default='pending')  # pending, verified, rejected
    admin_notes = db.Column(db.Text, nullable=True)
    verified_date = db.Column(db.String(20), nullable=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('payments', lazy=True))

