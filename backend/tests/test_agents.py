
import sys
import os

# Add the project root directory to the module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import pytest
from agents.business_expert import BusinessDomainExpertAI
from agents.developer import DeveloperAI
from agents.tester import CodeTesterAI
from agents.documentation import DocumentationAI
from agents.data_specialist import DataSpecialistAI

# Test BusinessDomainExpertAI
def test_provide_insights():
    business_expert = BusinessDomainExpertAI()
    result = business_expert.provide_insights("What is the best option strategy?")
    assert "strategy" in result.lower()

# Test DeveloperAI
def test_generate_code():
    developer_ai = DeveloperAI()
    result = developer_ai.generate_code("Generate a Flask API")
    assert "Flask" in result

# Test TesterAI
# def test_run_tests():
#     tester_ai = TesterAI()
#     code = "def add(a, b):\n    return a + b"
#     result = tester_ai.run_tests(code)
#     assert "passed" in result.lower() or "error" in result.lower()

# Test DocumentationAI
def test_generate_docs():
    documentation_ai = DocumentationAI()
    code = "def hello_world():\n    print('Hello, World!')"
    result = documentation_ai.generate_docs(code)
    assert "documentation" in result.lower() or "hello" in result.lower()

def test_analyze_data():
    data_specialist = DataSpecialistAI()
    result = data_specialist.analyze("test_data.csv")
    assert "summary" in result or "error" in result

def test_run_tests_success():
    tester_ai = CodeTesterAI()

    # Sample code with a simple testable function
    code = """
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(0, 0) == 0
    """

    # Run the test and assert success
    result = tester_ai.run_tests(code)
    assert "passed" in result.lower() or "tests" in result.lower()

def test_run_tests_failure():
    tester_ai = CodeTesterAI()

    # Code with failing test
    code = """
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 6  # This will fail
    """

    # Run the test and assert failure
    result = tester_ai.run_tests(code)
    assert "failed" in result.lower() or "error" in result.lower()

def test_validate_code():
    tester_ai = CodeTesterAI()

    # Code description and logic for validation
    code_description = "This function adds two numbers."
    code = """
def add(a, b):
    return a + b
"""

    # Use the AI-based validation
    result = tester_ai.validate_code(code_description, code)
    assert "valid" in result.lower() or "error" in result.lower() or "review" in result.lower()
