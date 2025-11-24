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

    def add_task(self, description: str, utility_score: int, cost_hours: float, deadline: Optional[str] = None, links: Optional[List[int]] = None) -> int:
        """
        Add a new task to the tasks list and save it to the file.

        :param description: Description of the task.
        :param utility_score: Utility score of the task (1-100).
        :param cost_hours: Cost in hours to complete the task.
        :param deadline: Optional deadline in YYYY-MM-DD format.
        :param links: Optional list of task IDs this task is linked to.
        :return: The ID of the newly created task.
        """
        new_id = max((task['id'] for task in self.tasks), default=0) + 1
        new_task = {
            'id': new_id,
            'description': description,
            'utility_score': utility_score,
            'cost_hours': cost_hours,
            'status': 'pending',
            'deadline': deadline,
            'linked_tasks': links or []
        }
        self.tasks.append(new_task)
        self.save_tasks()
        return new_id

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

    def get_task_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a task by its ID.

        :param task_id: ID of the task to retrieve.
        :return: The task dictionary if found, None otherwise.
        """
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None

    def link_tasks(self, task_id: int, linked_task_id: int) -> bool:
        """
        Link two tasks together. Creates a bidirectional relationship.

        :param task_id: ID of the first task.
        :param linked_task_id: ID of the task to link to.
        :return: True if successful, False if either task not found.
        """
        task = self.get_task_by_id(task_id)
        linked_task = self.get_task_by_id(linked_task_id)
        
        if not task or not linked_task:
            return False
        
        # Ensure linked_tasks field exists
        if 'linked_tasks' not in task:
            task['linked_tasks'] = []
        if 'linked_tasks' not in linked_task:
            linked_task['linked_tasks'] = []
        
        # Add bidirectional links (avoid duplicates)
        if linked_task_id not in task['linked_tasks']:
            task['linked_tasks'].append(linked_task_id)
        if task_id not in linked_task['linked_tasks']:
            linked_task['linked_tasks'].append(task_id)
        
        self.save_tasks()
        return True

    def unlink_tasks(self, task_id: int, linked_task_id: int) -> bool:
        """
        Remove the link between two tasks. Removes bidirectional relationship.

        :param task_id: ID of the first task.
        :param linked_task_id: ID of the task to unlink from.
        :return: True if successful, False if either task not found.
        """
        task = self.get_task_by_id(task_id)
        linked_task = self.get_task_by_id(linked_task_id)
        
        if not task or not linked_task:
            return False
        
        # Remove bidirectional links
        if 'linked_tasks' in task and linked_task_id in task['linked_tasks']:
            task['linked_tasks'].remove(linked_task_id)
        if 'linked_tasks' in linked_task and task_id in linked_task['linked_tasks']:
            linked_task['linked_tasks'].remove(task_id)
        
        self.save_tasks()
        return True

    def get_linked_tasks(self, task_id: int) -> List[Dict[str, Any]]:
        """
        Get all tasks linked to a specific task.

        :param task_id: ID of the task to get links for.
        :return: List of linked task dictionaries.
        """
        task = self.get_task_by_id(task_id)
        if not task or 'linked_tasks' not in task:
            return []
        
        linked_tasks = []
        for linked_id in task['linked_tasks']:
            linked_task = self.get_task_by_id(linked_id)
            if linked_task:
                linked_tasks.append(linked_task)
        
        return linked_tasks