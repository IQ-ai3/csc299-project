import argparse
import json
import os
from utils import read_tasks_from_file, write_tasks_to_file, generate_unique_id

TASKS_FILE = "../tasks.json"

def main():
    parser = argparse.ArgumentParser(description='Task Manager CLI with linking, editing, and completion')
    parser.add_argument('action', choices=['add', 'list', 'search', 'link', 'edit', 'complete'], help='Action to perform')
    parser.add_argument('--title', type=str, help='Title of the task (for add/edit)')
    parser.add_argument('--description', type=str, help='Description of the task (for add/edit)')
    parser.add_argument('--query', type=str, help='Keyword to search for in tasks')
    parser.add_argument('--links', type=str, help='Comma-separated IDs of linked tasks (for add/edit)')
    parser.add_argument('--id', type=int, help='Task ID (for edit/link/complete)')
    parser.add_argument('--linked_id', type=int, help='Task ID to link to (for link)')
    args = parser.parse_args()

    if args.action == 'add':
        if not args.title or not args.description:
            print("Error: Title and description are required to add a task.")
            return
        add_task(args.title, args.description, args.links)
    elif args.action == 'list':
        list_tasks()
    elif args.action == 'search':
        if not args.query:
            print("Error: --query is required for searching tasks.")
            return
        search_tasks(args.query)
    elif args.action == 'link':
        if args.id is None or args.linked_id is None:
            print("Error: --id and --linked_id are required for linking tasks.")
            return
        link_tasks(args.id, args.linked_id)
    elif args.action == 'edit':
        if args.id is None:
            print("Error: --id is required for editing a task.")
            return
        edit_task(args.id, args.title, args.description, args.links)
    elif args.action == 'complete':
        if args.id is None:
            print("Error: --id is required to complete a task.")
            return
        complete_task(args.id)

def handle_command(command, args):
    if command == "add":
        add_task(*args)
    elif command == "list":
        list_tasks()
    elif command == "search":
        if not args:
            print("Usage: python main.py search <keyword>")
            return
        search_tasks(args[0])
    elif command == "link":
        if len(args) < 2:
            print("Usage: python main.py link <task_id> <linked_task_id>")
            return
        link_tasks(int(args[0]), int(args[1]))
    elif command == "edit":
        if len(args) < 1:
            print("Usage: python main.py edit <task_id> [--title <title>] [--description <desc>] [--links <ids>]")
            return
        # For simplicity, only support title, description, links as positional args
        edit_task(int(args[0]), args[1] if len(args)>1 else None, args[2] if len(args)>2 else None, args[3] if len(args)>3 else None)
    elif command == "complete":
        if len(args) < 1:
            print("Usage: python main.py complete <task_id>")
            return
        complete_task(int(args[0]))
    else:
        print(f"Unknown command: {command}")

def add_task(title, description, links=None):
    tasks = read_tasks_from_file(TASKS_FILE)
    task = {
        "id": generate_unique_id(tasks),
        "title": title,
        "description": description,
        "links": [int(i) for i in links.split(",") if i.strip().isdigit()] if links else [],
        "completed": False
    }
    tasks.append(task)
    write_tasks_to_file(TASKS_FILE, tasks)
    print(f"Task added: {task}")

def list_tasks():
    tasks = read_tasks_from_file(TASKS_FILE)
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        links_str = ", ".join(str(l) for l in task.get("links", []))
        status = "[X]" if task.get("completed", False) else "[ ]"
        print(f"{status} [{task['id']}] {task['title']}: {task['description']} (Links: {links_str})")

def search_tasks(query):
    tasks = read_tasks_from_file(TASKS_FILE)
    query_lower = query.lower()
    results = [task for task in tasks if query_lower in task['title'].lower() or query_lower in task['description'].lower()]
    if not results:
        print(f"No tasks found matching: {query}")
        return
    for task in results:
        links_str = ", ".join(str(l) for l in task.get("links", []))
        status = "[X]" if task.get("completed", False) else "[ ]"
        print(f"{status} [{task['id']}] {task['title']}: {task['description']} (Links: {links_str})")
def complete_task(task_id):
    tasks = read_tasks_from_file(TASKS_FILE)
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            print(f"Task {task_id} marked as completed.")
            break
    else:
        print(f"Task {task_id} not found.")
        return
    write_tasks_to_file(TASKS_FILE, tasks)

def link_tasks(task_id, linked_id):
    tasks = read_tasks_from_file(TASKS_FILE)
    for task in tasks:
        if task['id'] == task_id:
            if 'links' not in task:
                task['links'] = []
            if linked_id not in task['links']:
                task['links'].append(linked_id)
                print(f"Linked task {linked_id} to task {task_id}.")
            else:
                print(f"Task {task_id} already linked to {linked_id}.")
            break
    else:
        print(f"Task {task_id} not found.")
        return
    write_tasks_to_file(TASKS_FILE, tasks)

def edit_task(task_id, title=None, description=None, links=None):
    tasks = read_tasks_from_file(TASKS_FILE)
    for task in tasks:
        if task['id'] == task_id:
            if title:
                task['title'] = title
            if description:
                task['description'] = description
            if links is not None:
                task['links'] = [int(i) for i in links.split(",") if i.strip().isdigit()]
            print(f"Task {task_id} updated: {task}")
            break
    else:
        print(f"Task {task_id} not found.")
        return
    write_tasks_to_file(TASKS_FILE, tasks)

if __name__ == '__main__':
    main()
