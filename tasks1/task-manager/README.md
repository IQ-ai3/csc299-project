# Task Manager CLI

A simple command-line interface task manager that allows users to add and list tasks. Tasks are stored in a JSON file for persistence.

## Features

- Add new tasks with a title and description.
- List all existing tasks.
- **Search tasks by keyword in title or description.**
- Tasks are saved in a `tasks.json` file in the root directory.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd task-manager
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

## Project Structure

```
task-manager
├── src
│   ├── main.py          # Entry point for the application
│   ├── cli.py           # Command-line interface logic
│   ├── task_manager.py   # Task management functionality
│   └── utils.py         # Utility functions for file handling
├── tasks.json           # JSON file storing tasks
├── specs
│   └── PLAN.md          # Project plan and architecture
├── requirements.txt      # Project dependencies
└── README.md            # Project documentation
```

## Contributing

Feel free to submit issues or pull requests for improvements and bug fixes.