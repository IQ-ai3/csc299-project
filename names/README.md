# CLI Task Manager

A simple JSON-backed command-line task manager supporting adding, listing, searching, editing, deleting, linking, and summarizing tasks.

## Features
- Add tasks with title, description, status, tags
- List all tasks
- Search by text, tag, or status
- Edit existing tasks
- Delete tasks (removes reciprocal links)
- Link / unlink tasks (bidirectional relationships)
- Show single task details
- Summary of status counts

## Data Model
```json
{
  "id": 1,
  "title": "Implement parser",
  "description": "Parse configuration files",
  "status": "open",
  "tags": ["core"],
  "links": [2],
  "created_at": "2025-11-19T12:00:00Z",
  "updated_at": "2025-11-19T12:00:00Z"
}
```
Stored in `.tasks.json` in current working directory.

## Installation
```powershell
python -m venv .venv; .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage Examples
```powershell
# Add tasks
python src/task_manager/cli.py add "Write docs" -d "Initial documentation" -t docs
python src/task_manager/cli.py add "Implement parser" -t core

# List
python src/task_manager/cli.py list

# Search
python src/task_manager/cli.py search -q parser
python src/task_manager/cli.py search -t docs
python src/task_manager/cli.py search -s open

# Edit
python src/task_manager/cli.py edit 1 -s done -d "Docs complete"

# Link tasks
python src/task_manager/cli.py link 1 2
python src/task_manager/cli.py show 1

# Unlink
python src/task_manager/cli.py unlink 1 2

# Delete
python src/task_manager/cli.py delete 2

# Summary
python src/task_manager/cli.py summary
```

## Testing
```powershell
.venv\Scripts\activate
pytest -q
```

## Notes
- Status values: open, in-progress, done, blocked
- Links are reciprocal; deleting a task cleans up inbound links.
- Corrupted `.tasks.json` is automatically backed up to `.tasks.json.bak`.
