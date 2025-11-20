import os
import tempfile
from src.task_manager.storage import TaskRepository


def make_repo():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()
    repo = TaskRepository(path=tmp.name)
    return repo, tmp.name


def cleanup(path):
    try:
        os.remove(path)
    except OSError:
        pass


def test_add_and_list():
    repo, path = make_repo()
    try:
        repo.add("Task A", "Desc", tags=["alpha"], status="open")
        repo.add("Task B", "", tags=["beta"], status="in-progress")
        tasks = repo.list()
        assert len(tasks) == 2
        assert tasks[0]["id"] == 1
        assert tasks[1]["id"] == 2
    finally:
        cleanup(path)


def test_edit_and_get():
    repo, path = make_repo()
    try:
        t = repo.add("Title", "Desc")
        repo.edit(t["id"], title="New Title", status="done")
        updated = repo.get(t["id"])
        assert updated["title"] == "New Title"
        assert updated["status"] == "done"
    finally:
        cleanup(path)


def test_delete_removes_and_unlinks():
    repo, path = make_repo()
    try:
        a = repo.add("A")
        b = repo.add("B")
        repo.link(a["id"], b["id"])
        repo.delete(a["id"])
        remaining = repo.get(b["id"])  # still exists
        assert remaining is not None
        assert a["id"] not in remaining["links"]
    finally:
        cleanup(path)


def test_search_by_text_and_tag():
    repo, path = make_repo()
    try:
        repo.add("Implement parser", "", tags=["core"], status="open")
        repo.add("Write docs", "", tags=["docs"], status="done")
        r1 = repo.search(text="parser")
        assert len(r1) == 1
        r2 = repo.search(tag="docs")
        assert len(r2) == 1
        r3 = repo.search(status="open")
        assert len(r3) == 1
    finally:
        cleanup(path)


def test_link_and_unlink():
    repo, path = make_repo()
    try:
        a = repo.add("A")
        b = repo.add("B")
        repo.link(a["id"], b["id"])
        assert b["id"] in repo.get(a["id"])["links"]
        assert a["id"] in repo.get(b["id"])["links"]
        repo.unlink(a["id"], b["id"])
        assert b["id"] not in repo.get(a["id"])["links"]
    finally:
        cleanup(path)
