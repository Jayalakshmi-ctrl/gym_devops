import pytest
from app import app

@pytest.fixture
def client():
    """Configures the Flask app for testing mode and creates a test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage_loads(client):
    """Test 1: Verify the homepage loads successfully (Status Code 200)."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"ACEest FUNCTIONAL FITNESS" in response.data
    assert b"Select a profile to view workout" in response.data

def test_fat_loss_program_selection(client):
    """Test 2: Verify selecting 'Fat Loss (FL)' returns the correct workout and diet details."""
    response = client.post('/', data={'program': 'Fat Loss (FL)'})
    assert response.status_code == 200
    assert b"5x5 Back Squat + AMRAP" in response.data
    assert b"Target: 2,000 kcal" in response.data

def test_muscle_gain_program_selection(client):
    """Test 3: Verify selecting 'Muscle Gain (MG)' returns the correct workout and diet details."""
    response = client.post('/', data={'program': 'Muscle Gain (MG)'})
    assert response.status_code == 200
    assert b"Squat 5x5" in response.data
    assert b"Target: 3,200 kcal" in response.data

def test_invalid_program_selection(client):
    """Test 4: Verify sending an invalid program does not crash the app."""
    response = client.post('/', data={'program': 'NonExistentProgram'})
    assert response.status_code == 200
    assert b"Select a profile to view workout" in response.data
