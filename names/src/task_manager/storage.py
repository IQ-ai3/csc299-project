import json
import os
import datetime
from typing import Any, Dict, List, Optional

TASK_FILE = os.path.join(os.getcwd(), ".tasks.json")
VALID_STATUSES = ["open", "in-progress", "done", "blocked"]

class TaskRepository:
    def __init__(self, path: str = TASK_FILE):
        self.path = path
        self._tasks: List[Dict[str, Any]] = []
        self._loaded = False

    def load(self) -> None:
        if self._loaded:
            return
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        self._tasks = data
                except json.JSONDecodeError:
                    # Corrupted file; start fresh but preserve a backup
                    backup = self.path + ".bak"
                    try:
                        os.replace(self.path, backup)
                    except OSError:
                        pass
                    self._tasks = []
        self._loaded = True

    def save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._tasks, f, indent=2)

    def _now(self) -> str:
        return datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"

    def _next_id(self) -> int:
        if not self._tasks:
            return 1
        return max(t["id"] for t in self._tasks) + 1

    def list(self) -> List[Dict[str, Any]]:
        self.load()
        return list(self._tasks)

    def get(self, task_id: int) -> Optional[Dict[str, Any]]:
        self.load()
        for t in self._tasks:
            if t["id"] == task_id:
                return t
        return None

    def add(self, title: str, description: str = "", status: str = "open", tags: Optional[List[str]] = None) -> Dict[str, Any]:
        self.load()
        if status not in VALID_STATUSES:
            raise ValueError(f"Invalid status '{status}'. Valid: {', '.join(VALID_STATUSES)}")
        now = self._now()
        task = {
            "id": self._next_id(),
            "title": title.strip(),
            "description": description.strip(),
            "status": status,
            "tags": tags or [],
            "links": [],
            "created_at": now,
            "updated_at": now,
        }
        self._tasks.append(task)
        self.save()
        return task

    def edit(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None, status: Optional[str] = None, tags: Optional[List[str]] = None) -> Dict[str, Any]:
        task = self.get(task_id)
        if not task:
            raise KeyError(f"Task {task_id} not found")
        changed = False
        if title is not None:
            task["title"] = title.strip(); changed = True
        if description is not None:
            task["description"] = description.strip(); changed = True
        if status is not None:
            if status not in VALID_STATUSES:
                raise ValueError(f"Invalid status '{status}'. Valid: {', '.join(VALID_STATUSES)}")
            task["status"] = status; changed = True
        if tags is not None:
            task["tags"] = tags; changed = True
        if changed:
            task["updated_at"] = self._now()
            self.save()
        return task

    def delete(self, task_id: int) -> bool:
        self.load()
        for i, t in enumerate(self._tasks):
            if t["id"] == task_id:
                # Remove links pointing to this task
                for other in self._tasks:
                    if task_id in other.get("links", []):
                        other["links"] = [lid for lid in other["links"] if lid != task_id]
                del self._tasks[i]
                self.save()
                return True
        return False

    def link(self, source_id: int, target_id: int) -> None:
        if source_id == target_id:
            raise ValueError("Cannot link a task to itself")
        source = self.get(source_id)
        target = self.get(target_id)
        if not source or not target:
            raise KeyError("Both tasks must exist to create a link")
        if target_id not in source["links"]:
            source["links"].append(target_id)
            source["updated_at"] = self._now()
        if source_id not in target["links"]:
            target["links"].append(source_id)
            target["updated_at"] = self._now()
        self.save()

    def unlink(self, source_id: int, target_id: int) -> None:
        source = self.get(source_id)
        target = self.get(target_id)
        if not source or not target:
            raise KeyError("Both tasks must exist to remove a link")
        if target_id in source["links"]:
            source["links"] = [lid for lid in source["links"] if lid != target_id]
            source["updated_at"] = self._now()
        if source_id in target["links"]:
            target["links"] = [lid for lid in target["links"] if lid != source_id]
            target["updated_at"] = self._now()
        self.save()

    def search(self, text: str = "", tag: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        self.load()
        terms = text.lower().split() if text else []
        result = []
        for t in self._tasks:
            if status and t["status"] != status:
                continue
            if tag and tag not in t.get("tags", []):
                continue
            if terms:
                hay = (t["title"] + " " + t["description"]).lower()
                if not all(term in hay for term in terms):
                    continue
            result.append(t)
        return result

    def summary(self) -> Dict[str, int]:
        self.load()
        out: Dict[str, int] = {s: 0 for s in VALID_STATUSES}
        for t in self._tasks:
            out[t["status"]] = out.get(t["status"], 0) + 1
        out["total"] = len(self._tasks)
        return out
