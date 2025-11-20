"""Task Manager package providing CLI-based task tracking.

Data Model (JSON persisted):
- id: int (auto-increment)
- title: str (required)
- description: str (optional)
- status: str (one of: open, in-progress, done, blocked)
- tags: list[str]
- links: list[int] (IDs of related tasks)
- created_at: ISO8601 string
- updated_at: ISO8601 string
"""
