import sys
import os

# Add the root directory to the module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_coordinator_finance(client):
    response = client.post('/coordinator', json={"query": "What is the best option strategy?"})
    data = response.get_json()
    assert response.status_code == 200
    assert "insights" in data["data"]
    assert "strategy" in data["data"]["insights"].lower()

def test_coordinator_code(client):
    response = client.post('/coordinator', json={"query": "Generate a Flask API"})
    data = response.get_json()
    assert response.status_code == 200
    assert "code" in data["data"]
    assert "Flask" in data["data"]["code"]

def test_coordinator_data_analysis(client):
    response = client.post('/coordinator', json={"query": "Analyze the test_data.csv file"})
    data = response.get_json()
    assert response.status_code == 200
    assert "data_analysis" in data["data"]
    assert "summary" in data["data"]["data_analysis"]
