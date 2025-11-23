import pytest
import os
import json
from typer.testing import CliRunner
from main import app
from task_manager import TaskManager

runner = CliRunner()

@pytest.fixture
def test_task_file(tmp_path):
    """Create a temporary tasks.json file for testing."""
    task_file = tmp_path / "test_tasks.json"
    return str(task_file)

@pytest.fixture
def task_manager_with_data(test_task_file):
    """Create a TaskManager with sample data."""
    manager = TaskManager(test_task_file)
    manager.add_task("Study microeconomics", 90, 5.0, "2025-12-01")
    manager.add_task("Complete Python assignment", 80, 3.0, "2025-11-25")
    manager.add_task("Read research paper", 60, 2.0)
    return manager

def test_add_command_without_deadline(test_task_file, monkeypatch):
    """Test adding a task without a deadline."""
    # Monkeypatch the task_manager in main.py
    import main
    monkeypatch.setattr(main, 'task_manager', TaskManager(test_task_file))
    
    result = runner.invoke(app, ["add", "Test task", "75", "4.5"])
    assert result.exit_code == 0
    assert "Task added successfully!" in result.stdout
    
    # Verify task was added
    with open(test_task_file, 'r') as f:
        tasks = json.load(f)
    assert len(tasks) == 1
    assert tasks[0]['description'] == "Test task"
    assert tasks[0]['utility_score'] == 75
    assert tasks[0]['cost_hours'] == 4.5
    assert tasks[0]['deadline'] is None

def test_add_command_with_deadline(test_task_file, monkeypatch):
    """Test adding a task with a deadline."""
    import main
    monkeypatch.setattr(main, 'task_manager', TaskManager(test_task_file))
    
    result = runner.invoke(app, ["add", "Study for exam", "95", "8.0", "--deadline", "2025-12-15"])
    assert result.exit_code == 0
    assert "Task added successfully!" in result.stdout
    
    # Verify task was added with deadline
    with open(test_task_file, 'r') as f:
        tasks = json.load(f)
    assert len(tasks) == 1
    assert tasks[0]['description'] == "Study for exam"
    assert tasks[0]['deadline'] == "2025-12-15"

def test_list_command_empty(test_task_file, monkeypatch):
    """Test listing tasks when no tasks exist."""
    import main
    monkeypatch.setattr(main, 'task_manager', TaskManager(test_task_file))
    
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "Tasks (Sorted by ROI - The Rational Choice)" in result.stdout

def test_list_command_with_tasks(test_task_file, monkeypatch):
    """Test listing tasks with data."""
    import main
    manager = TaskManager(test_task_file)
    manager.add_task("Task 1", 80, 4.0, "2025-12-01")
    manager.add_task("Task 2", 90, 3.0)
    monkeypatch.setattr(main, 'task_manager', manager)
    
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "Task 1" in result.stdout
    assert "Task 2" in result.stdout
    assert "ROI" in result.stdout
    assert "Deadline" in result.stdout

def test_list_command_roi_sorting(test_task_file, monkeypatch):
    """Test that tasks are sorted by ROI in descending order."""
    import main
    manager = TaskManager(test_task_file)
    # Task 1: ROI = 80/4 = 20
    manager.add_task("Low ROI Task", 80, 4.0)
    # Task 2: ROI = 90/3 = 30 (higher)
    manager.add_task("High ROI Task", 90, 3.0)
    monkeypatch.setattr(main, 'task_manager', manager)
    
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    # Higher ROI task should appear first
    high_roi_pos = result.stdout.find("High ROI Task")
    low_roi_pos = result.stdout.find("Low ROI Task")
    assert high_roi_pos < low_roi_pos

def test_delete_command_existing_task(test_task_file, monkeypatch):
    """Test deleting an existing task."""
    import main
    manager = TaskManager(test_task_file)
    manager.add_task("Task to delete", 70, 3.0)
    monkeypatch.setattr(main, 'task_manager', manager)
    
    result = runner.invoke(app, ["delete", "1"])
    assert result.exit_code == 0
    assert "Task 1 deleted successfully!" in result.stdout
    
    # Verify task was deleted
    with open(test_task_file, 'r') as f:
        tasks = json.load(f)
    assert len(tasks) == 0

def test_delete_command_nonexistent_task(test_task_file, monkeypatch):
    """Test deleting a task that doesn't exist."""
    import main
    monkeypatch.setattr(main, 'task_manager', TaskManager(test_task_file))
    
    result = runner.invoke(app, ["delete", "999"])
    assert result.exit_code == 0
    assert "Task 999 not found." in result.stdout

def test_search_command_found(test_task_file, monkeypatch):
    """Test searching for tasks with matching results."""
    import main
    manager = TaskManager(test_task_file)
    manager.add_task("Study Python programming", 85, 5.0)
    manager.add_task("Read economics textbook", 70, 3.0)
    manager.add_task("Python data analysis", 80, 4.0)
    monkeypatch.setattr(main, 'task_manager', manager)
    
    result = runner.invoke(app, ["search", "Python"])
    assert result.exit_code == 0
    assert "Search Results" in result.stdout
    assert "Study Python programming" in result.stdout
    assert "Python data analysis" in result.stdout
    assert "economics" not in result.stdout

def test_search_command_not_found(test_task_file, monkeypatch):
    """Test searching for tasks with no matching results."""
    import main
    manager = TaskManager(test_task_file)
    manager.add_task("Study microeconomics", 90, 5.0)
    monkeypatch.setattr(main, 'task_manager', manager)
    
    result = runner.invoke(app, ["search", "nonexistent"])
    assert result.exit_code == 0
    assert "No tasks found matching the query." in result.stdout

def test_search_command_case_insensitive(test_task_file, monkeypatch):
    """Test that search is case-insensitive."""
    import main
    manager = TaskManager(test_task_file)
    manager.add_task("Study Python Programming", 85, 5.0)
    monkeypatch.setattr(main, 'task_manager', manager)
    
    # Search with lowercase
    result = runner.invoke(app, ["search", "python"])
    assert result.exit_code == 0
    assert "Study Python Programming" in result.stdout
    
    # Search with uppercase
    result = runner.invoke(app, ["search", "PYTHON"])
    assert result.exit_code == 0
    assert "Study Python Programming" in result.stdout

def test_deadline_display_with_and_without(test_task_file, monkeypatch):
    """Test that deadlines display correctly for tasks with and without deadlines."""
    import main
    manager = TaskManager(test_task_file)
    manager.add_task("Task with deadline", 80, 4.0, "2025-12-01")
    manager.add_task("Task without deadline", 70, 3.0)
    monkeypatch.setattr(main, 'task_manager', manager)
    
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "2025-12-01" in result.stdout
    assert "N/A" in result.stdout
