"""
Test cases for the farming journal and crop planning models
"""
import pytest
import sys
import os
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import FarmingJournal, CropPlanning
from app import db

class TestFarmingJournal:
    """Test cases for FarmingJournal model"""
    
    def test_create_journal_entry(self, app, sample_journal_data):
        """Test creating a new journal entry"""
        with app.app_context():
            # Create journal entry
            journal = FarmingJournal(
                crop_type=sample_journal_data['crop_type'],
                date_planted=datetime.strptime(sample_journal_data['date_planted'], '%Y-%m-%d').date(),
                growth_stage=sample_journal_data['growth_stage'],
                weather_conditions=sample_journal_data['weather_conditions'],
                notes=sample_journal_data['notes'],
                water_amount=sample_journal_data['water_amount'],
                fertilizer_applied=sample_journal_data['fertilizer_applied']
            )
            
            db.session.add(journal)
            db.session.commit()
            
            # Verify the entry was created
            saved_journal = FarmingJournal.query.first()
            assert saved_journal is not None
            assert saved_journal.crop_type == sample_journal_data['crop_type']
            assert saved_journal.growth_stage == sample_journal_data['growth_stage']
            assert saved_journal.water_amount == sample_journal_data['water_amount']
    
    def test_journal_string_representation(self, app, sample_journal_data):
        """Test the string representation of journal entry"""
        with app.app_context():
            journal = FarmingJournal(
                crop_type=sample_journal_data['crop_type'],
                growth_stage=sample_journal_data['growth_stage']
            )
            
            expected_str = f"FarmingJournal('{sample_journal_data['crop_type']}', '{sample_journal_data['growth_stage']}')"
            assert str(journal) == expected_str
    
    def test_journal_query_by_crop_type(self, app, sample_journal_data):
        """Test querying journal entries by crop type"""
        with app.app_context():
            # Create multiple journal entries
            journal1 = FarmingJournal(crop_type='Tomato', growth_stage='Seedling')
            journal2 = FarmingJournal(crop_type='Tomato', growth_stage='Flowering')
            journal3 = FarmingJournal(crop_type='Corn', growth_stage='Mature')
            
            db.session.add_all([journal1, journal2, journal3])
            db.session.commit()
            
            # Query by crop type
            tomato_entries = FarmingJournal.query.filter_by(crop_type='Tomato').all()
            assert len(tomato_entries) == 2
            
            corn_entries = FarmingJournal.query.filter_by(crop_type='Corn').all()
            assert len(corn_entries) == 1

class TestCropPlanning:
    """Test cases for CropPlanning model"""
    
    def test_create_crop_plan(self, app, sample_crop_planning):
        """Test creating a new crop planning entry"""
        with app.app_context():
            crop_plan = CropPlanning(
                crop_name=sample_crop_planning['crop_name'],
                planting_season=sample_crop_planning['planting_season'],
                expected_yield=sample_crop_planning['expected_yield'],
                planning_notes=sample_crop_planning['planning_notes']
            )
            
            db.session.add(crop_plan)
            db.session.commit()
            
            # Verify the entry was created
            saved_plan = CropPlanning.query.first()
            assert saved_plan is not None
            assert saved_plan.crop_name == sample_crop_planning['crop_name']
            assert saved_plan.planting_season == sample_crop_planning['planting_season']
            assert saved_plan.expected_yield == sample_crop_planning['expected_yield']
    
    def test_crop_planning_string_representation(self, app, sample_crop_planning):
        """Test the string representation of crop planning entry"""
        with app.app_context():
            crop_plan = CropPlanning(
                crop_name=sample_crop_planning['crop_name'],
                planting_season=sample_crop_planning['planting_season']
            )
            
            expected_str = f"CropPlanning('{sample_crop_planning['crop_name']}', '{sample_crop_planning['planting_season']}')"
            assert str(crop_plan) == expected_str
    
    def test_crop_planning_query_by_season(self, app):
        """Test querying crop planning by season"""
        with app.app_context():
            # Create multiple crop planning entries
            plan1 = CropPlanning(crop_name='Tomato', planting_season='Spring')
            plan2 = CropPlanning(crop_name='Lettuce', planting_season='Spring')
            plan3 = CropPlanning(crop_name='Pumpkin', planting_season='Fall')
            
            db.session.add_all([plan1, plan2, plan3])
            db.session.commit()
            
            # Query by season
            spring_crops = CropPlanning.query.filter_by(planting_season='Spring').all()
            assert len(spring_crops) == 2
            
            fall_crops = CropPlanning.query.filter_by(planting_season='Fall').all()
            assert len(fall_crops) == 1
    
    def test_crop_planning_expected_yield_calculation(self, app):
        """Test expected yield calculations"""
        with app.app_context():
            crop_plan = CropPlanning(
                crop_name='Tomato',
                planting_season='Spring',
                expected_yield=75.5
            )
            
            db.session.add(crop_plan)
            db.session.commit()
            
            saved_plan = CropPlanning.query.first()
            assert saved_plan.expected_yield == 75.5
            assert isinstance(saved_plan.expected_yield, float)
