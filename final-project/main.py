import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from typing import Optional
from task_manager import TaskManager
from ai_summary import get_ai_task_summary

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
    table.add_column("Links", justify="center", style="cyan")

    for task, roi in tasks_with_roi:
        linked_count = len(task.get('linked_tasks', []))
        link_display = f"🔗 {linked_count}" if linked_count > 0 else "-"
        
        table.add_row(
            str(task['id']),
            task['description'],
            str(task['utility_score']),
            f"{task['cost_hours']:.2f}",
            f"{roi:.2f}",
            task.get('deadline') or 'N/A',
            link_display
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

@app.command()
def edit(
    task_id: int,
    description: Optional[str] = None,
    utility: Optional[int] = None,
    cost: Optional[float] = None,
    deadline: Optional[str] = None,
    status: Optional[str] = None
):
    """
    Edit a task's properties. Only provided fields will be updated.

    :param task_id: ID of the task to edit.
    :param description: New description for the task.
    :param utility: New utility score (1-100).
    :param cost: New cost in hours.
    :param deadline: New deadline in YYYY-MM-DD format.
    :param status: New status (pending/complete).
    """
    updates = {}
    if description is not None:
        updates['description'] = description
    if utility is not None:
        updates['utility_score'] = utility
    if cost is not None:
        updates['cost_hours'] = cost
    if deadline is not None:
        updates['deadline'] = deadline
    if status is not None:
        updates['status'] = status
    
    if not updates:
        console.print("No updates provided. Please specify at least one field to update.", style="yellow")
        return
    
    if task_manager.edit_task(task_id, **updates):
        console.print(f"Task {task_id} updated successfully!", style="green")
        console.print(f"Updated fields: {', '.join(updates.keys())}", style="cyan")
    else:
        console.print(f"Task {task_id} not found.", style="red")

@app.command()
def ai_summary():
    """
    Generate an AI-powered summary of your tasks using OpenAI's API.
    Requires OPENAI_API_KEY environment variable to be set.
    """
    summary = get_ai_task_summary(task_manager.tasks)
    console.print(Panel(summary, title="🤖 AI Task Analysis", border_style="blue"))

@app.command()
def link(task_id: int, linked_task_id: int):
    """
    Link two tasks together to show their relationship.

    :param task_id: ID of the first task.
    :param linked_task_id: ID of the task to link to.
    """
    if task_id == linked_task_id:
        console.print("Cannot link a task to itself.", style="red")
        return
    
    if task_manager.link_tasks(task_id, linked_task_id):
        console.print(f"✓ Tasks {task_id} and {linked_task_id} are now linked!", style="green")
    else:
        console.print(f"Failed to link tasks. Check that both task IDs exist.", style="red")

@app.command()
def unlink(task_id: int, linked_task_id: int):
    """
    Remove the link between two tasks.

    :param task_id: ID of the first task.
    :param linked_task_id: ID of the task to unlink from.
    """
    if task_manager.unlink_tasks(task_id, linked_task_id):
        console.print(f"✓ Tasks {task_id} and {linked_task_id} are now unlinked.", style="green")
    else:
        console.print(f"Failed to unlink tasks. Check that both task IDs exist.", style="red")

@app.command()
def view(task_id: int):
    """
    View detailed information about a specific task, including linked tasks.

    :param task_id: ID of the task to view.
    """
    task = task_manager.get_task_by_id(task_id)
    
    if not task:
        console.print(f"Task {task_id} not found.", style="red")
        return
    
    # Calculate ROI
    roi = task['utility_score'] / task['cost_hours'] if task['cost_hours'] != 0 else 0
    
    # Create details panel
    details = f"""
[bold cyan]ID:[/bold cyan] {task['id']}
[bold magenta]Description:[/bold magenta] {task['description']}
[bold green]Utility Score:[/bold green] {task['utility_score']}
[bold yellow]Cost (Hours):[/bold yellow] {task['cost_hours']:.2f}
[bold blue]ROI:[/bold blue] {roi:.2f}
[bold red]Deadline:[/bold red] {task.get('deadline') or 'N/A'}
[bold white]Status:[/bold white] {task['status']}
"""
    
    # Add linked tasks information
    linked_tasks = task_manager.get_linked_tasks(task_id)
    if linked_tasks:
        details += "\n[bold]🔗 Linked Tasks:[/bold]\n"
        for linked in linked_tasks:
            details += f"  • Task {linked['id']}: {linked['description']}\n"
    else:
        details += "\n[dim]No linked tasks[/dim]"
    
    console.print(Panel(details, title=f"📋 Task Details", border_style="cyan"))

if __name__ == "__main__":
    app()