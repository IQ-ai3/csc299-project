import typer
from rich.console import Console
from rich.table import Table
from typing import Optional
from task_manager import TaskManager

app = typer.Typer()
console = Console()

task_manager = TaskManager("tasks.json")

@app.command()
def add(description: str, utility: int, cost: float, deadline: Optional[str] = None):
    """
    Add a new task with the given description, utility, cost, and optional deadline.

    :param description: Description of the task.
    :param utility: Utility score of the task (1-100).
    :param cost: Cost in hours to complete the task.
    :param deadline: Optional deadline in YYYY-MM-DD format.
    """
    task_manager.add_task(description, utility, cost, deadline)
    console.print(f"Task added successfully!", style="green")

@app.command()
def list():
    """
    List all tasks with their ROI (utility / cost), sorted by highest ROI first.
    """
    tasks = task_manager.tasks
    
    # Calculate ROI for each task and sort by ROI descending
    tasks_with_roi = []
    for task in tasks:
        utility = task['utility_score']
        cost = task['cost_hours']
        roi = utility / cost if cost != 0 else 0
        tasks_with_roi.append((task, roi))
    
    # Sort by ROI descending (highest ROI first - The Rational Choice)
    tasks_with_roi.sort(key=lambda x: x[1], reverse=True)
    
    table = Table(title="Tasks (Sorted by ROI - The Rational Choice)")
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Description", style="magenta")
    table.add_column("Utility", justify="right", style="green")
    table.add_column("Cost (Hrs)", justify="right", style="yellow")
    table.add_column("ROI", justify="right", style="blue")
    table.add_column("Deadline", justify="center", style="red")

    for task, roi in tasks_with_roi:
        table.add_row(
            str(task['id']),
            task['description'],
            str(task['utility_score']),
            f"{task['cost_hours']:.2f}",
            f"{roi:.2f}",
            task.get('deadline') or 'N/A'
        )

    console.print(table)

@app.command()
def delete(task_id: int):
    """
    Delete a task by its ID.

    :param task_id: ID of the task to delete.
    """
    if task_manager.delete_task(task_id):
        console.print(f"Task {task_id} deleted successfully!", style="green")
    else:
        console.print(f"Task {task_id} not found.", style="red")

@app.command()
def search(query: str):
    """
    Search for tasks containing the given query string.

    :param query: Query string to search for in task descriptions.
    """
    results = task_manager.search_tasks(query)
    if not results:
        console.print("No tasks found matching the query.", style="red")
        return

    table = Table(title="Search Results")
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Description", style="magenta")
    table.add_column("Utility", justify="right", style="green")
    table.add_column("Cost (Hrs)", justify="right", style="yellow")
    table.add_column("Deadline", justify="center", style="red")

    for task in results:
        table.add_row(
            str(task['id']),
            task['description'],
            str(task['utility_score']),
            f"{task['cost_hours']:.2f}",
            task.get('deadline') or 'N/A'
        )

    console.print(table)

if __name__ == "__main__":
    app()