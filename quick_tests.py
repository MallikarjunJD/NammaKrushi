#!/usr/bin/env python3
"""
Quick Test Runner for Hackathon Demo
===================================

This is a simplified test runner that focuses on the most critical 
functionality for your hackathon presentation.

Usage:
    python quick_tests.py

What it tests:
- Core API endpoints
- Database operations
- ML predictions
- AI alerts generation
"""

import unittest
import json
import sys
import os
from unittest.mock import patch, MagicMock

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import app, db
from app.models import User, Task, Inventory, Expense, Journal

class QuickTestSuite(unittest.TestCase):
    """Essential tests for hackathon demo"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment once"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        
        cls.client = app.test_client()
        cls.app_context = app.app_context()
        cls.app_context.push()
        
        db.create_all()
        
        # Create test user
        cls.test_user = User(username='demo_user', password='demo123')
        db.session.add(cls.test_user)
        db.session.commit()
        
        print("🚀 Quick test environment ready!")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test environment"""
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()
        print("✅ Test cleanup complete!")
    
    def setUp(self):
        """Login before each test"""
        with self.client.session_transaction() as sess:
            sess['user_id'] = self.test_user.id
    
    def test_001_user_registration(self):
        """Test 1: User can register successfully"""
        response = self.client.post('/register', data={
            'signupName': 'hackathon_user',
            'signupPassword': 'secure123',
            'signupConfirm': 'secure123'
        })
        self.assertEqual(response.status_code, 302)
        
        user = User.query.filter_by(username='hackathon_user').first()
        self.assertIsNotNone(user)
        print("✅ Test 1: User Registration - PASSED")
    
    def test_002_task_management(self):
        """Test 2: Task CRUD operations work"""
        # Add task
        response = self.client.post('/add_task', data={
            'taskTitle': 'Demo Task',
            'taskDate': '2025-09-15',
            'taskNotes': 'For hackathon demo'
        })
        self.assertEqual(response.status_code, 302)
        
        # Get tasks
        response = self.client.get('/get_tasks')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('tasks', data)
        
        print("✅ Test 2: Task Management - PASSED")
    
    def test_003_inventory_api(self):
        """Test 3: Inventory API functionality"""
        response = self.client.post('/api/inventory', 
                                  json={'item': 'Demo Seeds', 'quantity': 100})
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        print("✅ Test 3: Inventory API - PASSED")
    
    def test_004_farming_journal(self):
        """Test 4: Farming journal works"""
        response = self.client.post('/api/journal', 
                                  json={
                                      'activity': 'watering',
                                      'activity_details': 'Demo watering activity',
                                      'date': '2025-09-10'
                                  })
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        print("✅ Test 4: Farming Journal - PASSED")
    
    def test_005_ml_predictions(self):
        """Test 5: ML crop predictions work"""
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
        print("✅ Test 5: ML Predictions - PASSED")
    
    @patch('openai.OpenAI')
    def test_006_ai_alerts(self, mock_openai):
        """Test 6: AI farming alerts generation"""
        # Add journal entry for analysis
        entry = Journal(activity='watering', activity_details='Test', 
                       date='2025-09-08', user_id=self.test_user.id)
        db.session.add(entry)
        db.session.commit()
        
        # Mock OpenAI
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices[0].message.content = json.dumps([{
            "type": "info",
            "icon": "💧",
            "title": "Demo Alert",
            "message": "This is a demo AI alert",
            "priority": "medium"
        }])
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        response = self.client.get('/api/farming_alerts')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        print("✅ Test 6: AI Alerts - PASSED")
    
    @patch('requests.get')
    def test_007_weather_integration(self, mock_get):
        """Test 7: Weather API integration"""
        # Mock weather response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'list': [{
                'dt_txt': '2025-09-10 12:00:00',
                'main': {'temp': 28.5, 'humidity': 65},
                'weather': [{'description': 'sunny'}],
                'pop': 0.1
            }]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        response = self.client.get('/api/weather_forecast')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        print("✅ Test 7: Weather Integration - PASSED")
    
    def test_008_seasonal_report(self):
        """Test 8: Seasonal reports generate properly"""
        response = self.client.get('/api/seasonal_report')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        print("✅ Test 8: Seasonal Reports - PASSED")


def run_quick_tests():
    """Run quick test suite for hackathon demo"""
    print("\n" + "="*60)
    print("🎯 HACKATHON QUICK TEST SUITE")
    print("="*60)
    print("Testing core functionality for demo...")
    print()
    
    # Run tests
    suite = unittest.TestLoader().loadTestsFromTestCase(QuickTestSuite)
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)
    
    # Results
    total = result.testsRun
    passed = total - len(result.failures) - len(result.errors)
    
    print("\n" + "="*60)
    print("📊 QUICK TEST RESULTS")
    print("="*60)
    print(f"Tests Run: {total}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {len(result.failures + result.errors)}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if result.failures or result.errors:
        print("\n❌ Issues Found:")
        for test, error in result.failures + result.errors:
            print(f"  - {test}: {error.split('AssertionError:')[-1].strip()}")
    else:
        print("\n🎉 ALL TESTS PASSED!")
        print("🚀 Ready for hackathon demo!")
    
    print("="*60)
    return passed == total


if __name__ == '__main__':
    success = run_quick_tests()
    sys.exit(0 if success else 1)
