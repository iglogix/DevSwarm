#!/bin/bash

# Create Project Directories
echo "Creating project directories..."
mkdir -p agents tests utils

# Create Main Application Files
echo "Creating main application files..."
touch app.py requirements.txt config.py

# Create Agent Files
echo "Creating agent files..."
touch agents/__init__.py
touch agents/coordinator.py
touch agents/business_expert.py
touch agents/developer.py
touch agents/tester.py
touch agents/documentation.py
touch agents/data_specialist.py

# Create Utility Files
echo "Creating utility files..."
touch utils/__init__.py
touch utils/logger.py
touch utils/validator.py

# Create Test Files
echo "Creating test files..."
touch tests/__init__.py
touch tests/test_app.py
touch tests/test_agents.py

# Add Boilerplate Content
echo "Adding boilerplate content..."

# app.py
# cat <<EOL > app.py
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from agents.coordinator import CoordinatorAI

# app = Flask(__name__)
# CORS(app)

# @app.route('/coordinator', methods=['POST'])
# def coordinator():
#     try:
#         user_request = request.json.get("query", "")
#         coordinator_ai = CoordinatorAI()
#         response = coordinator_ai.handle_request(user_request)
#         return jsonify(response)
#     except Exception as e:
#         return jsonify({"status": "error", "errors": [str(e)]}), 500

# if __name__ == '__main__':
#     app.run(debug=True)
# EOL

# requirements.txt
cat <<EOL > requirements.txt
flask
flask-cors
openai
pytest
EOL

# config.py
cat <<EOL > config.py
OPENAI_API_KEY = "your-openai-api-key"
EOL

# logger.py
cat <<EOL > utils/logger.py
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CoordinatorAI")

def log_message(message):
    logger.info(message)
EOL

# validator.py
cat <<EOL > utils/validator.py
def validate_request(data):
    if not data or "query" not in data:
        return False, "Invalid input: 'query' field is required."
    return True, None
EOL

# coordinator.py
cat <<EOL > agents/coordinator.py
from agents.business_expert import BusinessDomainExpertAI
from agents.developer import DeveloperAI
from agents.tester import TesterAI
from agents.documentation import DocumentationAI
from agents.data_specialist import DataSpecialistAI

class CoordinatorAI:
    def __init__(self):
        self.business_expert = BusinessDomainExpertAI()
        self.developer = DeveloperAI()
        self.tester = TesterAI()
        self.documentation = DocumentationAI()
        self.data_specialist = DataSpecialistAI()

    def handle_request(self, user_request):
        response = {"status": "processing", "data": {}, "errors": []}

        try:
            if "finance" in user_request.lower():
                response["data"]["insights"] = self.business_expert.provide_insights(user_request)
            elif "code" in user_request.lower():
                code = self.developer.generate_code(user_request)
                response["data"]["code"] = code
                response["data"]["tests"] = self.tester.run_tests(code)
                response["data"]["documentation"] = self.documentation.generate_docs(code)
            elif "data" in user_request.lower():
                response["data"]["data_analysis"] = self.data_specialist.analyze(user_request)
            else:
                response["errors"].append("Unknown request type")

            response["status"] = "completed"
        except Exception as e:
            response["status"] = "error"
            response["errors"].append(str(e))

        return response
EOL

# Create empty Python files for agents
for agent in business_expert developer tester documentation data_specialist; do
    echo "class ${agent^}AI:
    def __init__(self):
        pass" > agents/${agent}.py
done

# Add basic test cases
cat <<EOL > tests/test_app.py
import pytest
from project.app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_coordinator_endpoint(client):
    response = client.post('/coordinator', json={"query": "Generate a Flask API"})
    assert response.status_code == 200
EOL

cat <<EOL > tests/test_agents.py
import pytest
from project.agents.developer import DeveloperAI

def test_generate_code():
    developer_ai = DeveloperAI()
    result = developer_ai.generate_code("Generate a Flask API")
    assert "Flask" in result
EOL

# Complete
echo "Project structure created successfully!"
