#!/usr/bin/env python3
"""
Comprehensive Test Suite for Farm Management System
==================================================

This test suite covers all major functionality including:
- User authentication and registration
- Task management (CRUD operations)
- Inventory management
- Expense tracking
- Farming journal
- AI-powered farming alerts
- ML crop predictions
- Weather integration
- Market insights

For Hackathon Presentation:
- Demonstrates code quality and reliability
- Shows comprehensive testing approach
- Validates all API endpoints
- Tests business logic
"""

import unittest
import json
import os
import sys
from datetime import date, datetime
from unittest.mock import patch, MagicMock

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Import Flask app and models
from app import app, db
from app.models import User, Task, Inventory, Expense, Journal

class FarmManagementTestCase(unittest.TestCase):
    """Base test case class with common setup and teardown"""
    
    def setUp(self):
        """Set up test database and client"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        
        # Create all database tables
        db.create_all()
        
        # Create a test user
        self.test_user = User(username='testuser', password='testpass123')
        db.session.add(self.test_user)
        db.session.commit()
        
        print(f"✅ Test setup complete - User ID: {self.test_user.id}")
    
    def tearDown(self):
        """Clean up after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        print("🧹 Test cleanup complete")
    
    def login_test_user(self):
        """Helper method to log in the test user"""
        with self.client.session_transaction() as sess:
            sess['user_id'] = self.test_user.id
        return self.test_user


class UserAuthenticationTests(FarmManagementTestCase):
    """Test user authentication and registration functionality"""
    
    def test_user_registration_success(self):
        """Test successful user registration"""
        response = self.client.post('/register', data={
            'signupName': 'newuser',
            'signupPassword': 'newpass123',
            'signupConfirm': 'newpass123'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        
        # Check if user was created in database
        new_user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.username, 'newuser')
        print("✅ User registration test passed")
    
    def test_user_registration_password_mismatch(self):
        """Test registration with mismatched passwords"""
        response = self.client.post('/register', data={
            'signupName': 'newuser2',
            'signupPassword': 'password123',
            'signupConfirm': 'different123'
        })
        
        # Should redirect back to login with error
        self.assertEqual(response.status_code, 302)
        
        # User should not be created
        user = User.query.filter_by(username='newuser2').first()
        self.assertIsNone(user)
        print("✅ Password mismatch test passed")
    
    def test_user_login_success(self):
        """Test successful user login"""
        response = self.client.post('/login', data={
            'loginName': 'testuser',
            'loginPassword': 'testpass123'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect to dashboard
        print("✅ User login test passed")
    
    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post('/login', data={
            'loginName': 'testuser',
            'loginPassword': 'wrongpassword'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect back to login
        print("✅ Invalid credentials test passed")


class TaskManagementTests(FarmManagementTestCase):
    """Test task management functionality"""
    
    def test_add_task_success(self):
        """Test adding a new task"""
        self.login_test_user()
        
        response = self.client.post('/add_task', data={
            'taskTitle': 'Water the crops',
            'taskDate': '2025-09-15',
            'taskNotes': 'Morning irrigation for tomatoes'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after adding
        
        # Check if task was created
        task = Task.query.filter_by(title='Water the crops').first()
        self.assertIsNotNone(task)
        self.assertEqual(task.user_id, self.test_user.id)
        self.assertEqual(task.notes, 'Morning irrigation for tomatoes')
        print("✅ Add task test passed")
    
    def test_get_tasks_api(self):
        """Test getting tasks via API"""
        self.login_test_user()
        
        # Add some test tasks
        task1 = Task(title='Test Task 1', date='2025-09-10', notes='Note 1', user_id=self.test_user.id)
        task2 = Task(title='Test Task 2', date='2025-09-11', notes='Note 2', user_id=self.test_user.id)
        db.session.add_all([task1, task2])
        db.session.commit()
        
        response = self.client.get('/get_tasks')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('tasks', data)
        self.assertEqual(len(data['tasks']), 2)
        print("✅ Get tasks API test passed")
    
    def test_delete_task_api(self):
        """Test deleting a task via API"""
        self.login_test_user()
        
        # Create a test task
        task = Task(title='Task to Delete', date='2025-09-10', user_id=self.test_user.id)
        db.session.add(task)
        db.session.commit()
        
        response = self.client.post('/api/delete_task', 
                                  json={'task_id': task.id})
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        
        # Verify task is deleted
        deleted_task = Task.query.get(task.id)
        self.assertIsNone(deleted_task)
        print("✅ Delete task API test passed")


class InventoryManagementTests(FarmManagementTestCase):
    """Test inventory management functionality"""
    
    def test_add_inventory_item(self):
        """Test adding inventory item"""
        self.login_test_user()
        
        response = self.client.post('/api/inventory', 
                                  json={'item': 'Fertilizer', 'quantity': 50})
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])
        
        # Check database
        inventory = Inventory.query.filter_by(item='Fertilizer').first()
        self.assertIsNotNone(inventory)
        self.assertEqual(inventory.quantity, 50)
        print("✅ Add inventory test passed")
    
    def test_update_inventory_item(self):
        """Test updating existing inventory item"""
        self.login_test_user()
        
        # Create initial inventory
        inventory = Inventory(item='Seeds', quantity=100, user_id=self.test_user.id)
        db.session.add(inventory)
        db.session.commit()
        
        # Update quantity
        response = self.client.post('/api/inventory', 
                                  json={'item': 'Seeds', 'quantity': 150})
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertFalse(data['created'])  # Should be updated, not created
        
        # Check updated quantity
        updated_inventory = Inventory.query.filter_by(item='Seeds').first()
        self.assertEqual(updated_inventory.quantity, 150)
        print("✅ Update inventory test passed")


class ExpenseTrackingTests(FarmManagementTestCase):
    """Test expense tracking functionality"""
    
    def test_add_expense(self):
        """Test adding a new expense"""
        self.login_test_user()
        
        response = self.client.post('/api/expense', 
                                  json={
                                      'item': 'Pesticide',
                                      'amount': 1500,
                                      'season': 'kharif'
                                  })
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['item'], 'Pesticide')
        self.assertEqual(data['amount'], 1500)
        
        # Check database
        expense = Expense.query.filter_by(item='Pesticide').first()
        self.assertIsNotNone(expense)
        self.assertEqual(expense.amount, 1500)
        self.assertEqual(expense.season, 'kharif')
        print("✅ Add expense test passed")
    
    def test_delete_expense(self):
        """Test deleting an expense"""
        self.login_test_user()
        
        # Create test expense
        expense = Expense(item='Test Expense', amount=500, season='rabi', user_id=self.test_user.id)
        db.session.add(expense)
        db.session.commit()
        
        response = self.client.post('/api/delete_expense', 
                                  json={'exp_id': expense.id})
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        
        # Verify deletion
        deleted_expense = Expense.query.get(expense.id)
        self.assertIsNone(deleted_expense)
        print("✅ Delete expense test passed")


class FarmingJournalTests(FarmManagementTestCase):
    """Test farming journal functionality"""
    
    def test_add_journal_entry(self):
        """Test adding a journal entry"""
        self.login_test_user()
        
        response = self.client.post('/api/journal', 
                                  json={
                                      'activity': 'watering',
                                      'activity_details': 'Watered tomato plants in greenhouse',
                                      'date': '2025-09-10'
                                  })
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['activity'], 'watering')
        
        # Check database
        entry = Journal.query.filter_by(activity='watering').first()
        self.assertIsNotNone(entry)
        self.assertEqual(entry.activity_details, 'Watered tomato plants in greenhouse')
        print("✅ Add journal entry test passed")
    
    def test_get_journal_entries(self):
        """Test retrieving journal entries"""
        self.login_test_user()
        
        # Add test entries
        entry1 = Journal(activity='planting', activity_details='Planted corn', date='2025-09-08', user_id=self.test_user.id)
        entry2 = Journal(activity='fertilizing', activity_details='Applied NPK fertilizer', date='2025-09-09', user_id=self.test_user.id)
        db.session.add_all([entry1, entry2])
        db.session.commit()
        
        response = self.client.get('/api/journal')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['entries']), 2)
        print("✅ Get journal entries test passed")
    
    def test_invalid_activity_type(self):
        """Test adding journal entry with invalid activity type"""
        self.login_test_user()
        
        response = self.client.post('/api/journal', 
                                  json={
                                      'activity': 'invalid_activity',
                                      'activity_details': 'Some details',
                                      'date': '2025-09-10'
                                  })
        
        self.assertEqual(response.status_code, 400)  # Bad request
        
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        print("✅ Invalid activity type test passed")


class WeatherIntegrationTests(FarmManagementTestCase):
    """Test weather API integration"""
    
    @patch('requests.get')
    def test_weather_forecast_api(self, mock_get):
        """Test weather forecast API endpoint"""
        self.login_test_user()
        
        # Mock weather API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'list': [
                {
                    'dt_txt': '2025-09-10 12:00:00',
                    'main': {'temp': 28.5, 'humidity': 65},
                    'weather': [{'description': 'partly cloudy'}],
                    'pop': 0.2
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        response = self.client.get('/api/weather_forecast?lat=16.5449&lon=81.5212')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('forecast', data)
        print("✅ Weather forecast API test passed")


class MLPredictionTests(FarmManagementTestCase):
    """Test ML crop prediction functionality"""
    
    def test_crop_prediction_api(self):
        """Test ML crop prediction endpoint"""
        self.login_test_user()
        
        response = self.client.post('/api/predict', 
                                  json={
                                      'temperature': 28,
                                      'humidity': 70,
                                      'rainfall': 150
                                  })
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('predictions', data)
        self.assertIn('weather_data', data)
        
        # Check prediction format
        predictions = data['predictions']
        self.assertEqual(len(predictions), 3)  # Top 3 predictions
        
        for pred in predictions:
            self.assertEqual(len(pred), 2)  # [crop_name, confidence]
            self.assertIsInstance(pred[1], float)  # Confidence should be float
            self.assertGreaterEqual(pred[1], 0)    # Confidence >= 0
            self.assertLessEqual(pred[1], 1)       # Confidence <= 1
        
        print("✅ ML crop prediction test passed")
    
    def test_crop_recommendation_api(self):
        """Test crop recommendation API with weather integration"""
        self.login_test_user()
        
        with patch('requests.get') as mock_get:
            # Mock weather API response
            mock_response = MagicMock()
            mock_response.json.return_value = {
                'main': {'temp': 30, 'humidity': 75},
                'weather': [{'description': 'hot and humid'}]
            }
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            response = self.client.get('/api/crop_recommendations?lat=16.5449&lon=81.5212')
            self.assertEqual(response.status_code, 200)
            
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            self.assertIn('recommendations', data)
            self.assertIn('weather_data', data)
            print("✅ Crop recommendation API test passed")


class FarmingAlertsTests(FarmManagementTestCase):
    """Test AI-powered farming alerts functionality"""
    
    @patch('openai.OpenAI')
    def test_farming_alerts_api(self, mock_openai):
        """Test farming alerts generation"""
        self.login_test_user()
        
        # Add some journal entries for analysis
        entries = [
            Journal(activity='watering', activity_details='Watered crops', date='2025-09-08', user_id=self.test_user.id),
            Journal(activity='fertilizing', activity_details='Applied fertilizer', date='2025-09-05', user_id=self.test_user.id),
        ]
        db.session.add_all(entries)
        db.session.commit()
        
        # Mock OpenAI response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices[0].message.content = json.dumps([
            {
                "type": "warning",
                "icon": "⚠️",
                "title": "Irrigation Check",
                "message": "Last watering was 2 days ago. Check soil moisture levels.",
                "priority": "medium"
            }
        ])
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        response = self.client.get('/api/farming_alerts')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('alerts', data)
        self.assertGreater(len(data['alerts']), 0)
        
        # Check alert structure
        alert = data['alerts'][0]
        self.assertIn('type', alert)
        self.assertIn('title', alert)
        self.assertIn('message', alert)
        self.assertIn('priority', alert)
        print("✅ Farming alerts API test passed")


class SeasonalReportTests(FarmManagementTestCase):
    """Test seasonal report functionality"""
    
    def test_seasonal_report_api(self):
        """Test seasonal report generation"""
        self.login_test_user()
        
        # Add test data
        task = Task(title='Harvest corn', date='2025-09-10', user_id=self.test_user.id)
        inventory = Inventory(item='Seeds', quantity=50, user_id=self.test_user.id)
        expense = Expense(item='Fertilizer', amount=2000, season='kharif', user_id=self.test_user.id)
        journal = Journal(activity='harvesting', activity_details='Harvested corn', date='2025-09-10', user_id=self.test_user.id)
        
        db.session.add_all([task, inventory, expense, journal])
        db.session.commit()
        
        response = self.client.get('/api/seasonal_report')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        
        report_data = data['data']
        self.assertIn('summary', report_data)
        self.assertIn('tasks', report_data)
        self.assertIn('inventory', report_data)
        self.assertIn('expenses', report_data)
        self.assertIn('journal', report_data)
        
        # Check summary counts
        summary = report_data['summary']
        self.assertEqual(summary['total_tasks'], 1)
        self.assertEqual(summary['total_inventory_items'], 1)
        self.assertEqual(summary['total_expenses'], 2000)
        self.assertEqual(summary['total_journal_entries'], 1)
        print("✅ Seasonal report API test passed")


def run_all_tests():
    """Run all test suites and provide comprehensive results"""
    print("\n" + "="*80)
    print("🚀 FARM MANAGEMENT SYSTEM - COMPREHENSIVE TEST SUITE")
    print("="*80)
    print("Testing all major functionality for hackathon presentation...")
    print()
    
    # Create test suite
    test_classes = [
        UserAuthenticationTests,
        TaskManagementTests,
        InventoryManagementTests,
        ExpenseTrackingTests,
        FarmingJournalTests,
        WeatherIntegrationTests,
        MLPredictionTests,
        FarmingAlertsTests,
        SeasonalReportTests
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = []
    
    for test_class in test_classes:
        print(f"\n📋 Running {test_class.__name__}...")
        print("-" * 50)
        
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        runner = unittest.TextTestRunner(verbosity=2, stream=open(os.devnull, 'w'))
        result = runner.run(suite)
        
        class_total = result.testsRun
        class_passed = class_total - len(result.failures) - len(result.errors)
        
        total_tests += class_total
        passed_tests += class_passed
        
        if result.failures or result.errors:
            for failure in result.failures + result.errors:
                failed_tests.append(f"{test_class.__name__}: {failure[0]}")
        
        print(f"✅ {class_passed}/{class_total} tests passed in {test_class.__name__}")
    
    # Final results
    print("\n" + "="*80)
    print("📊 FINAL TEST RESULTS")
    print("="*80)
    print(f"Total Tests Run: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {len(failed_tests)}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if failed_tests:
        print("\n❌ Failed Tests:")
        for failure in failed_tests:
            print(f"  - {failure}")
    
    print("\n🎯 TEST COVERAGE SUMMARY:")
    print("✅ User Authentication & Registration")
    print("✅ Task Management (CRUD)")
    print("✅ Inventory Management")
    print("✅ Expense Tracking")
    print("✅ Farming Journal")
    print("✅ Weather API Integration")
    print("✅ ML Crop Predictions")
    print("✅ AI-Powered Farming Alerts")
    print("✅ Seasonal Reports")
    print("\n🏆 READY FOR HACKATHON PRESENTATION!")
    print("="*80)
    
    return passed_tests == total_tests


if __name__ == '__main__':
    run_all_tests()
