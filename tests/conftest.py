import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import FarmingJournal, CropPlanning

@pytest.fixture
def app():
    """Create application for testing"""
    # Mock environment variables
    with patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test-openai-key',
        'GOOGLE_GEMINI_API_KEY': 'test-gemini-key'
    }):
        app = create_app()
        app.config.update({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'WTF_CSRF_ENABLED': False
        })
        
        with app.app_context():
            db.create_all()
            yield app
            db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create test runner"""
    return app.test_cli_runner()

@pytest.fixture
def sample_journal_data():
    """Sample farming journal data for testing"""
    return {
        'crop_type': 'Tomato',
        'date_planted': '2024-01-15',
        'growth_stage': 'Flowering',
        'weather_conditions': 'Sunny, 25°C',
        'notes': 'Plants showing good growth. Need to check for pests.',
        'water_amount': 10.5,
        'fertilizer_applied': 'NPK 10-10-10'
    }

@pytest.fixture
def sample_crop_planning():
    """Sample crop planning data for testing"""
    return {
        'crop_name': 'Tomato',
        'planting_season': 'Spring',
        'expected_yield': 50.0,
        'planning_notes': 'High-value crop for market sale'
    }
