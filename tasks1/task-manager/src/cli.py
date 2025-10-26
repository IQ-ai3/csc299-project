import argparse
import json
import os

TASKS_FILE = "../tasks.json"

def main():
    parser = argparse.ArgumentParser(description='Simple Task Manager CLI')
    parser.add_argument('action', choices=['add', 'list'], help='Action to perform: add a task or list tasks')
    parser.add_argument('--title', type=str, help='Title of the task (required for adding a task)')
    parser.add_argument('--description', type=str, help='Description of the task (required for adding a task)')

    args = parser.parse_args()

    if args.action == 'add':
        if not args.title or not args.description:
            print("Error: Title and description are required to add a task.")
            return
        add_task(args.title, args.description)
        print(f"Task added: {args.title}")
    elif args.action == 'list':
        list_tasks()
        print("Tasks listed.")

def handle_command(command, args):
    if command == "add":
        add_task(args)
    elif command == "list":
        list_tasks()
    else:
        print(f"Unknown command: {command}")

def add_task(args):
    if len(args) < 2:
        print("Usage: python main.py add <title> <description>")
        return
    title, description = args[0], args[1]
    task = {"id": get_next_id(), "title": title, "description": description}
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added: {task}")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        print(f"[{task['id']}] {task['title']}: {task['description']}")

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []  # Return an empty list if the file is empty or invalid

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def get_next_id():
    tasks = load_tasks()
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1

if __name__ == '__main__':
    main()