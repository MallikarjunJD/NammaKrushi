# 🌾 NammaKrushi - Farm Management & Marketplace System

A comprehensive AI-powered farm management platform that helps farmers optimize their operations, connect with markets, and make data-driven decisions using climate insights and machine learning.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Setup](#environment-setup)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🌤️ **Climate-Smart Crop Planning**
- **AI Crop Recommendations**: Get personalized crop suggestions based on:
  - Real-time weather data (temperature, humidity, rainfall)
  - Soil conditions and regional climate patterns
  - Market demand and price predictions
- **Season-Aware Crop Calendar**: Dynamic activity schedules (Kharif, Rabi, Zaid seasons)
- **Risk Analysis**: Color-coded risk bands for different crops
- **Market Insights**: AI-generated price trends and demand forecasts
- **PDF Reports**: Download detailed crop planning reports

### 📊 **Smart Dashboard**
- **Task Management**: Create, track, and get email reminders for farm tasks
- **Inventory Tracking**: Monitor seeds, fertilizers, equipment, and livestock
- **Expense Management**: Track costs with category-wise breakdown
- **Farm Journal**: Document daily activities and observations
- **AI Farming Alerts**: Get intelligent recommendations based on your journal entries
- **Weather Integration**: Real-time weather updates for your location

### 🛒 **Farmer Marketplace**
- **Product Listings**: 
  - Sell crops, equipment, seeds, and livestock
  - Upload product images
  - Set prices and quantities
  - Track inventory automatically
- **Seller Verification**: Admin-approved verified seller badges
- **Shopping Cart**: Add products, adjust quantities, checkout
- **Payment Integration**: Razorpay payment gateway with UPI/card support
- **Order Tracking**: Real-time order status updates (Pending → Verified → Delivered)
- **SMS Notifications**: Twilio integration sends SMS to sellers when orders are verified

### 📈 **Seasonal Analytics**
- **Comprehensive Reports**: 
  - Activity tracking and trends
  - Expense analysis by category
  - Task completion rates
  - Inventory status
- **Data Visualizations**: Charts for expenses, activities, and inventory
- **PDF Export**: Download formatted seasonal reports
- **AI-Powered Insights**: Gemini AI generates personalized farming recommendations

### 🤖 **AI Assistant**
- **Climate-Smart Chatbot**: Ask questions about:
  - Crop planning and pest management
  - Weather-based farming advice
  - Seasonal best practices
  - Market trends
- **Powered by OpenAI GPT-3.5**: Natural language understanding
- **Context-Aware**: Provides region and season-specific advice

### 👨‍💼 **Admin Panel**
- **Product Moderation**: Approve/reject marketplace listings
- **Seller Verification**: Verify farmer credentials
- **Payment Management**: Verify payment screenshots and update order status
- **User Management**: Monitor platform activity

---

## 🛠️ Tech Stack

### **Backend**
- **Flask** (Python 3.13) - Web framework
- **SQLAlchemy** - ORM for database management
- **Flask-Login** - User authentication
- **SQLite** - Database (development)

### **AI/ML**
- **OpenAI GPT-3.5** - Chatbot and crop recommendations
- **Google Gemini 1.5 Flash** - Enhanced farming insights
- **NumPy** - Data processing

### **External APIs**
- **OpenWeather API** - Real-time weather data
- **Razorpay** - Payment processing
- **Twilio** - SMS notifications

### **Frontend**
- **HTML5/CSS3/JavaScript** - UI components
- **Fetch API** - Asynchronous requests
- **Responsive Design** - Mobile-friendly interface

### **Other Tools**
- **ReportLab** - PDF generation
- **python-dotenv** - Environment variable management
- **bcrypt** - Password hashing

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+** ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **pip** (comes with Python)

### Installation

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/MallikarjunJD/NammKrushi.git

```

#### 2️⃣ Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Setup

#### 4️⃣ Configure Environment Variables

Create a `.env` file in the root directory by copying the example:

```bash
cp .env.example .env
```

Edit `.env` with your actual credentials:

```env
# Security Keys
FARM_SECURITY_KEY=your_random_secure_key_here
SECRET_KEY=your_flask_secret_key_here

# Database
DATABASE_URL=sqlite:///app.db

# OpenAI API (Required for AI features)
OPENAI_API_KEY=sk-proj-YOUR_OPENAI_API_KEY_HERE

# Google Gemini AI (Optional)
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE

# Weather API (Required for weather features)
WEATHER_API_KEY=YOUR_OPENWEATHER_API_KEY_HERE

# Twilio SMS (Optional - for order notifications)
TWILIO_ACCOUNT_SID=YOUR_TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN=YOUR_TWILIO_AUTH_TOKEN
TWILIO_PHONE_NUMBER=+1234567890

# Email Configuration (Optional - for task reminders)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_specific_password
RECEIVER_EMAIL=recipient@gmail.com
```

**Where to Get API Keys:**

- **OpenAI**: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Gemini**: [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
- **OpenWeather**: [openweathermap.org/api](https://openweathermap.org/api)
- **Twilio**: [twilio.com/console](https://www.twilio.com/console)
- **Gmail App Password**: [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

#### 5️⃣ Initialize Database

```bash
python recreate_db.py
```

This creates the SQLite database with all required tables.

#### 6️⃣ Create Admin User (Optional)

```bash
python create_admin.py
```

Follow the prompts to create an admin account for marketplace management.

---

## 📱 Usage Guide

### Running the Application

```bash
python run.py
```

The application will start on `http://localhost:5000`

### First-Time Setup

1. **Register an Account**
   - Navigate to `http://localhost:5000`
   - Click "Register" 
   - Fill in your details (username, email, password, location)
   - Click "Create Account"

2. **Login**
   - Use your credentials to log in
   - You'll be redirected to the dashboard

3. **Explore Features**

#### 🌾 Dashboard
- Add tasks with deadlines
- Log inventory items
- Track expenses
- Write journal entries
- View weather updates
- Get AI farming alerts

#### 🛒 Marketplace
- **Buy Products**: Browse listings, add to cart, checkout
- **Sell Products**: 
  - Click "My Listings" tab
  - Fill product details (name, category, price, quantity, image URL)
  - Wait for admin approval
  - View orders for your products

#### 📊 Seasonal Report
- View comprehensive analytics
- Download PDF reports
- Get AI-powered recommendations

#### 🌱 Crop Planning
- Enter weather parameters
- Get crop recommendations
- View market insights
- Download planning reports

#### 🤖 Climate Assistant
- Ask farming questions
- Get weather-based advice
- Learn about seasonal practices

---

## 📁 Project Structure

```
Hackathon/
├── app/
│   ├── __init__.py           # Flask app initialization
│   ├── models.py             # Database models
│   ├── routes.py             # API routes and views
│   ├── static/               # CSS, JS, images
│   └── templates/            # HTML templates
│       ├── login.html
│       ├── dashboard.html
│       ├── marketplace.html
│       ├── seasonal_report.html
│       ├── crop_planning.html
│       ├── climate_smart_assistant.html
│       └── admin.html
├── instance/
│   └── app.db                # SQLite database
├── migrations/               # Database migrations
├── venv/                     # Virtual environment
├── .env                      # Environment variables (DO NOT COMMIT)
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
├── requirements.txt          # Python dependencies
├── run.py                    # Application entry point
├── config.py                 # Configuration settings
└── README.md                 # This file
```

---

## 🔌 API Documentation

### Authentication Endpoints

```
POST /api/register         - Register new user
POST /api/login           - User login
POST /api/logout          - User logout
```

### Dashboard APIs

```
GET  /api/tasks           - Get user tasks
POST /api/tasks           - Create task
PUT  /api/tasks/<id>      - Update task
DELETE /api/tasks/<id>    - Delete task

GET  /api/inventory       - Get inventory
POST /api/inventory       - Add inventory
DELETE /api/inventory/<id> - Delete inventory

GET  /api/expenses        - Get expenses
POST /api/expenses        - Add expense
DELETE /api/expenses/<id> - Delete expense

GET  /api/journal         - Get journal entries
POST /api/journal         - Add journal entry
```

### Marketplace APIs

```
GET  /api/products                    - Get all approved products
POST /api/products                    - Create product listing
GET  /api/user_products               - Get user's products
GET  /api/product_orders/<id>         - Get orders for product
POST /api/payment                     - Create payment record
GET  /api/user_orders                 - Get user's orders
```

### Admin APIs

```
GET  /api/admin/products              - Get pending products
POST /api/admin/approve_product       - Approve product
POST /api/admin/reject_product        - Reject product
GET  /api/admin/verification_requests - Get verification requests
POST /api/admin/approve_verification  - Approve seller
POST /api/admin/reject_verification   - Reject seller
GET  /api/admin/payments              - Get payment records
POST /api/admin/verify_payment        - Verify payment
POST /api/admin/reject_payment        - Reject payment
```

### AI/Analytics APIs

```
POST /api/predict_crops               - Get crop recommendations
POST /api/crop_calendar              - Generate crop calendar
POST /api/climate_smart_chat         - Chatbot interaction
GET  /api/seasonal_report            - Get analytics report
GET  /api/seasonal_report_pdf        - Download PDF report
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Add comments for complex logic
- Update README if adding new features
- Test changes before submitting PR
- Never commit `.env` files or API keys

---

## 🔒 Security Notes

- **Never commit `.env` files** - They contain sensitive API keys
- **Use strong passwords** - Minimum 8 characters with uppercase, lowercase, and numbers
- **Rotate API keys** regularly if exposed
- **HTTPS in production** - Use SSL certificates for deployment
- **Environment variables** - Always use `.env` for secrets

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

## 🙏 Acknowledgments

- **OpenAI** - GPT-3.5 for AI features
- **Google** - Gemini AI for enhanced insights
- **OpenWeather** - Weather data API
- **Twilio** - SMS notifications
- **Razorpay** - Payment gateway
- **Flask Community** - Excellent documentation

---

## 📞 Support

For issues or questions:

- **GitHub Issues**: [github.com/MallikarjunJD/NammaKrushi/issues](https://github.com/MallikarjunJD/NammaKrushi/issues)
- **Email**: mallikarjunjadi9@gmail.com

---

## 🎯 Roadmap

- [ ] Mobile app (React Native)
- [ ] Real ML model for crop prediction
- [ ] Multi-language support
- [ ] IoT sensor integration
- [ ] Community forum
- [ ] Weather alerts
- [ ] Crop disease detection (Computer Vision)
- [ ] Marketplace analytics for sellers

---

**Made with ❤️ for farmers by Team BOLDVISIONS**
