import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_status(client):
    response = client.get('/status')
    assert response.status_code == 200

def test_process(client):
    response = client.post('/process', json={"prompt": "What is AI?"})
    assert response.status_code == 200
    assert "response" in response.get_json()["data"]
