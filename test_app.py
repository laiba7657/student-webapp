import pytest
import json
from app import app, init_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    init_db()
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test home page returns 200"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Student Portal' in response.data

def test_get_students(client):
    """Test students endpoint returns JSON"""
    response = client.get('/students')
    assert response.status_code == 200
    assert response.content_type == 'application/json'

def test_add_student(client):
    """Test adding a student"""
    payload = {"name": "Ali Khan", "grade": "A"}
    response = client.post('/add',
                           data=json.dumps(payload),
                           content_type='application/json')
    assert response.status_code == 201
    assert b'Student added' in response.data

def test_invalid_route(client):
    """Test 404 on invalid route"""
    response = client.get('/nonexistent')
    assert response.status_code == 404