import subprocess
import json
import os
import pytest

# File to store names
DATA_FILE = "names.json"

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Ensure a clean environment before and after each test."""
    # Remove the data file if it exists
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    yield
    # Cleanup after the test
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)

def test_add_name():
    """Test adding a name using the CLI."""
    result = subprocess.run(
        ["python", "main.py", "add", "John Doe"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Added: John Doe" in result.stdout

def test_list_names():
    """Test listing names using the CLI."""
    names = ["Jane Smith", "John Doe"]
    with open(DATA_FILE, "w") as f:
        json.dump(names, f)
    result = subprocess.run(
        ["python", "main.py", "list-names"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Jane Smith" in result.stdout
    assert "John Doe" in result.stdout