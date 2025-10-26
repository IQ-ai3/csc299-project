class TaskManager:
    def __init__(self, storage_file='tasks.json'):
        self.storage_file = storage_file
        self.tasks = self.load_tasks()

    def load_tasks(self):
        import json
        try:
            with open(self.storage_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        import json
        with open(self.storage_file, 'w') as file:
            json.dump(self.tasks, file)

    def add_task(self, title, description):
        task_id = self.generate_id()
        task = {
            'id': task_id,
            'title': title,
            'description': description
        }
        self.tasks.append(task)
        self.save_tasks()

    def list_tasks(self):
        return self.tasks

    def generate_id(self):
        import uuid
        return str(uuid.uuid4())