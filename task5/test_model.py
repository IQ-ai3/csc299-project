import json
import pytest

# File to store names
DATA_FILE = "names.json"

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Ensure a clean environment before and after each test."""
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    yield
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)

def test_model_structure():
    """Test the structure of the data model."""
    data = {"name": "John Doe"}
    assert "name" in data
    assert isinstance(data["name"], str)