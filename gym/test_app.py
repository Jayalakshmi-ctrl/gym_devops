import pytest
from app import app

@pytest.fixture
def client():
    """Configures the Flask app environment for isolated pipeline integration checks."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage_loads_successfully(client):
    """Test 1: Verify the premium dark theme base dashboard page loads (Status 200)."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"ACEest FUNCTIONAL FITNESS SYSTEM" in response.data
    assert b"Select a profile to view workout" in response.data

def test_dynamic_calorie_calculation_math(client):
    """Test 2: Verify dynamic calorie factors evaluate exactly matching math parameters (80kg * 35 multiplier)."""
    response = client.post('/', data={
        'name': 'Jayalakshmi',
        'age': '35',
        'weight': '80',
        'program': 'Muscle Gain (MG)',
        'adherence': '80',
        'action': 'refresh'  # Emulates picking a dropdown program menu selection
    })
    assert response.status_code == 200
    # 80 kg * 35 calorie_factor = 2800 kcal
    assert b"2800 kcal" in response.data
    assert b"Mon: Squat 5x5" in response.data

def test_save_client_validation_success(client):
    """Test 3: Verify form handles complete client profiles and displays success alerts."""
    response = client.post('/', data={
        'name': 'Deshpande',
        'age': '24',
        'weight': '65',
        'program': 'Fat Loss (FL)',
        'adherence': '95',
        'action': 'save'
    })
    assert response.status_code == 200
    assert b"Saved: Client Deshpande saved successfully. Adherence: 95%" in response.data

def test_incomplete_field_validation_catch(client):
    """Test 4: Verify field restrictions prevent missing inputs from creating a transaction."""
    response = client.post('/', data={
        'name': '',  # Empty name parameter violates programmatic validation limits
        'program': 'Beginner (BG)',
        'action': 'save'
    })
    assert response.status_code == 200
    assert b"Incomplete: Please fill client name and program." in response.data
