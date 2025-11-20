import json
import os
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

def test_storage_write():
    """Test writing to the storage."""
    data = ["John Doe"]
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)
    with open(DATA_FILE, "r") as f:
        loaded_data = json.load(f)
    assert loaded_data == data

def test_storage_read():
    """Test reading from the storage."""
    data = ["Jane Smith"]
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)
    with open(DATA_FILE, "r") as f:
        loaded_data = json.load(f)
    assert loaded_data == data