"""
Test cases for the farming application routes and API endpoints
"""
import pytest
import json
import sys
import os
from unittest.mock import patch, Mock

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import FarmingJournal, CropPlanning
from app import db

class TestRoutes:
    """Test cases for application routes"""
    
    def test_index_route(self, client):
        """Test the main index route"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Farm Management System' in response.data or b'Welcome' in response.data
    
    def test_crop_planning_route(self, client):
        """Test the crop planning route"""
        response = client.get('/crop_planning')
        assert response.status_code == 200
    
    def test_farming_journal_route(self, client):
        """Test the farming journal route"""
        response = client.get('/farming_journal')
        assert response.status_code == 200

class TestFarmingJournalAPI:
    """Test cases for farming journal API endpoints"""
    
    def test_add_journal_entry_valid_data(self, client, app, sample_journal_data):
        """Test adding a valid journal entry"""
        with app.app_context():
            response = client.post('/add_journal_entry', 
                                 data=sample_journal_data,
                                 follow_redirects=True)
            
            # Should redirect successfully
            assert response.status_code == 200
            
            # Verify entry was added to database
            journal = FarmingJournal.query.filter_by(crop_type=sample_journal_data['crop_type']).first()
            assert journal is not None
            assert journal.growth_stage == sample_journal_data['growth_stage']
    
    def test_add_journal_entry_missing_data(self, client):
        """Test adding journal entry with missing required data"""
        incomplete_data = {
            'crop_type': 'Tomato'
            # Missing other required fields
        }
        
        response = client.post('/add_journal_entry', data=incomplete_data)
        
        # Should handle missing data gracefully
        assert response.status_code in [200, 302, 400]
    
    @patch('app.routes.requests.get')
    def test_get_weather_data_success(self, mock_get, client):
        """Test successful weather data retrieval"""
        # Mock successful weather API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'current': {
                'temperature_2m': 25.5,
                'relative_humidity_2m': 65,
                'precipitation': 0.0,
                'wind_speed_10m': 10.2
            }
        }
        mock_get.return_value = mock_response
        
        response = client.get('/api/weather?lat=40.7128&lon=-74.0060')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'weather' in data
        assert data['weather']['temperature'] == 25.5
    
    @patch('app.routes.requests.get')
    def test_get_weather_data_failure(self, mock_get, client):
        """Test weather data retrieval failure"""
        # Mock failed weather API response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        response = client.get('/api/weather?lat=40.7128&lon=-74.0060')
        assert response.status_code == 200  # Should handle gracefully
        
        data = json.loads(response.data)
        assert 'error' in data

class TestCropPlanningAPI:
    """Test cases for crop planning API endpoints"""
    
    def test_add_crop_plan_valid_data(self, client, app, sample_crop_planning):
        """Test adding a valid crop planning entry"""
        with app.app_context():
            response = client.post('/add_crop_plan', 
                                 data=sample_crop_planning,
                                 follow_redirects=True)
            
            # Should redirect successfully
            assert response.status_code == 200
            
            # Verify entry was added to database
            crop_plan = CropPlanning.query.filter_by(crop_name=sample_crop_planning['crop_name']).first()
            assert crop_plan is not None
            assert crop_plan.planting_season == sample_crop_planning['planting_season']

class TestAIIntegration:
    """Test cases for AI integration endpoints"""
    
    @patch('app.routes.openai.ChatCompletion.create')
    def test_farming_alerts_openai_success(self, mock_openai, client, app):
        """Test farming alerts with successful OpenAI response"""
        with app.app_context():
            # Create test journal entry
            journal = FarmingJournal(
                crop_type='Tomato',
                growth_stage='Flowering',
                weather_conditions='Hot and dry',
                notes='Plants looking stressed'
            )
            db.session.add(journal)
            db.session.commit()
            
            # Mock OpenAI response
            mock_openai.return_value.choices = [
                Mock(message=Mock(content='{"alerts": ["Water plants more frequently", "Check for heat stress"]}'))
            ]
            
            response = client.get('/api/farming_alerts')
            assert response.status_code == 200
            
            data = json.loads(response.data)
            assert 'alerts' in data
            assert len(data['alerts']) > 0
    
    @patch('app.routes.genai.GenerativeModel')
    def test_farming_alerts_gemini_success(self, mock_gemini, client, app):
        """Test farming alerts with successful Gemini response"""
        with app.app_context():
            # Create test journal entry
            journal = FarmingJournal(
                crop_type='Corn',
                growth_stage='Mature',
                weather_conditions='Rainy',
                notes='Ready for harvest'
            )
            db.session.add(journal)
            db.session.commit()
            
            # Mock Gemini response
            mock_model = Mock()
            mock_model.generate_content.return_value.text = '{"alerts": ["Harvest corn before more rain", "Check grain moisture"]}'
            mock_gemini.return_value = mock_model
            
            response = client.get('/api/farming_alerts')
            assert response.status_code == 200
            
            data = json.loads(response.data)
            assert 'alerts' in data
            assert 'ai_source' in data
    
    @patch('app.routes.genai.GenerativeModel')
    def test_smart_calendar_success(self, mock_gemini, client, app):
        """Test smart calendar generation with Gemini"""
        with app.app_context():
            # Create test crop planning entry
            crop_plan = CropPlanning(
                crop_name='Tomato',
                planting_season='Spring',
                expected_yield=50.0
            )
            db.session.add(crop_plan)
            db.session.commit()
            
            # Mock Gemini response
            mock_model = Mock()
            mock_model.generate_content.return_value.text = '''
            {
                "calendar_activities": [
                    {
                        "date": "2024-03-15",
                        "activity": "Plant tomato seeds",
                        "priority": "high",
                        "estimated_duration": "2 hours"
                    }
                ]
            }
            '''
            mock_gemini.return_value = mock_model
            
            response = client.get('/api/smart_calendar')
            assert response.status_code == 200
            
            data = json.loads(response.data)
            assert 'calendar_activities' in data
            assert len(data['calendar_activities']) > 0

class TestErrorHandling:
    """Test cases for error handling"""
    
    def test_nonexistent_route(self, client):
        """Test accessing a non-existent route"""
        response = client.get('/nonexistent')
        assert response.status_code == 404
    
    @patch('app.routes.openai.ChatCompletion.create')
    @patch('app.routes.genai.GenerativeModel')
    def test_ai_failure_fallback(self, mock_gemini, mock_openai, client, app):
        """Test AI failure fallback behavior"""
        with app.app_context():
            # Mock both AI services to fail
            mock_gemini.side_effect = Exception("Gemini API error")
            mock_openai.side_effect = Exception("OpenAI API error")
            
            response = client.get('/api/farming_alerts')
            assert response.status_code == 200
            
            data = json.loads(response.data)
            # Should return fallback alerts
            assert 'alerts' in data
            assert 'ai_source' in data
            assert data['ai_source'] == 'fallback'

class TestDataValidation:
    """Test cases for data validation"""
    
    def test_journal_entry_date_validation(self, client):
        """Test journal entry with invalid date format"""
        invalid_data = {
            'crop_type': 'Tomato',
            'date_planted': 'invalid-date',
            'growth_stage': 'Seedling'
        }
        
        response = client.post('/add_journal_entry', data=invalid_data)
        # Should handle invalid date gracefully
        assert response.status_code in [200, 302, 400]
    
    def test_crop_planning_yield_validation(self, client):
        """Test crop planning with invalid yield value"""
        invalid_data = {
            'crop_name': 'Tomato',
            'planting_season': 'Spring',
            'expected_yield': 'not-a-number'
        }
        
        response = client.post('/add_crop_plan', data=invalid_data)
        # Should handle invalid yield gracefully
        assert response.status_code in [200, 302, 400]
