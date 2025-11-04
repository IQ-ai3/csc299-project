# Task Manager CLI (tasks2)

A command-line task manager with task linking and editing features.

## Features

- Add new tasks with a title and description.
- List all existing tasks.
- Search tasks by keyword in title or description.
- **Link tasks together (dependencies, references, etc).**
- **Edit tasks (update title, description, links).**
- Tasks are saved in a `tasks.json` file in the root directory.

## Installation

1. Clone the repository:
   ```
   git clone <repo-url>
   ```
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the task manager, use the following command:

```
python src/main.py
```

### Commands

- **Add a Task**:
  ```
  python src/main.py add "Task Title" "Task Description"
  ```
- **List Tasks**:
  ```
  python src/main.py list
  ```
- **Search Tasks**:
  ```
  python src/main.py search "keyword"
  ```

**Link Tasks**:
  ```
  python src/main.py link <task_id> <linked_task_id>
  ```
  Example: Link task 2 to task 1
  ```
  python src/main.py link 1 2
  ```

**Edit Task**:
  ```
  python src/main.py edit <task_id> --title "New Title" --description "New Description" --links "2,3"
  ```
  Example: Edit task 1's title and description
  ```
  python src/main.py edit 1 --title "Updated Title" --description "Updated Description"
  ```
  Example: Edit task 1's links
  ```
  python src/main.py edit 1 --links "2,3"
  ```

**Mark Task as Completed**:
  ```
  python src/main.py complete --id <task_id>
  ```
  Example: Mark task 1 as completed
  ```
  python src/main.py complete --id 1
  ```

Feel free to submit issues or pull requests for improvements and bug fixes.
