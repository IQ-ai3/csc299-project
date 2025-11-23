import json
from typing import List, Dict, Any, Optional

class TaskManager:
    """
    A class to manage tasks stored in a local tasks.json file.
    """

    def __init__(self, file_path: str):
        """
        Initialize the TaskManager with the path to the tasks.json file.

        :param file_path: Path to the tasks.json file.
        """
        self.file_path = file_path
        self.tasks: List[Dict[str, Any]] = []
        self.load_tasks()

    def load_tasks(self) -> None:
        """
        Load tasks from the JSON file. Handles FileNotFoundError.
        """
        try:
            with open(self.file_path, 'r') as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self) -> None:
        """
        Save the current tasks to the JSON file.
        """
        with open(self.file_path, 'w') as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self, description: str, utility_score: int, cost_hours: float, deadline: Optional[str] = None) -> None:
        """
        Add a new task to the tasks list and save it to the file.

        :param description: Description of the task.
        :param utility_score: Utility score of the task (1-100).
        :param cost_hours: Cost in hours to complete the task.
        :param deadline: Optional deadline in YYYY-MM-DD format.
        """
        new_id = max((task['id'] for task in self.tasks), default=0) + 1
        new_task = {
            'id': new_id,
            'description': description,
            'utility_score': utility_score,
            'cost_hours': cost_hours,
            'status': 'pending',
            'deadline': deadline
        }
        self.tasks.append(new_task)
        self.save_tasks()

    def search_tasks(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Search for tasks containing the given keyword (case-insensitive).

        :param keyword: Keyword to search for in task descriptions.
        :return: List of tasks containing the keyword.
        """
        return [task for task in self.tasks if keyword.lower() in task['description'].lower()]

    def edit_task(self, task_id: int, **kwargs) -> bool:
        """
        Edit a task's fields by its ID.

        :param task_id: ID of the task to edit.
        :param kwargs: Fields to update (e.g., utility_score, status).
        :return: True if the task was updated, False if not found.
        """
        for task in self.tasks:
            if task['id'] == task_id:
                task.update(kwargs)
                self.save_tasks()
                return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        :param task_id: ID of the task to delete.
        :return: True if the task was deleted, False if not found.
        """
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                del self.tasks[i]
                self.save_tasks()
                return True
        return False

    def get_best_tasks(self) -> List[Dict[str, Any]]:
        """
        Get pending tasks sorted by utility-to-cost ratio in descending order.

        :return: List of pending tasks sorted by (utility_score / cost_hours).
        """
        pending_tasks = [task for task in self.tasks if task['status'] == 'pending']
        return sorted(pending_tasks, key=lambda x: x['utility_score'] / x['cost_hours'], reverse=True)