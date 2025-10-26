def read_tasks_from_file(file_path):
    import json
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def write_tasks_to_file(file_path, tasks):
    import json
    with open(file_path, 'w') as file:
        json.dump(tasks, file, indent=4)

def generate_unique_id(tasks):
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1