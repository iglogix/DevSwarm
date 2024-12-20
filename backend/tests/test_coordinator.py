import sys
import os

# Add the root directory to the module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app
from agents.coordinator import CoordinatorAI

# @pytest.fixture
def test_handle_request():
    coordinator = CoordinatorAI()
    user_request = "Create a Flask API with database integration and tests"

    response = coordinator.handle_request(user_request)

    assert response["status"] == "completed"
    assert len(response["data"]) > 0
    for subtask in response["data"]:
        assert "result" in subtask