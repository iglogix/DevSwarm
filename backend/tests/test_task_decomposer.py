import sys
import os
import unittest
# Add the root directory to the module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.task_decomposer import TaskDecomposerAI

def test_print():
    print("hello")

def test_decompose():
    task_decomposer = TaskDecomposerAI()
    query = "Create stock data analyzer app with access to database and polygon api"

    subtasks = task_decomposer.decompose(query)

    print(subtasks)

    assert isinstance(subtasks, list)
    assert len(subtasks) > 0
    for subtask in subtasks:
        assert "task" in subtask
        assert "details" in subtask
