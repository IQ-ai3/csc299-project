import sys
import pathlib

# Ensure src directory is importable
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

import cli
import utils

def test_add_and_list(tmp_path, capsys):
    fp = tmp_path / "tasks.json"
    # point CLI to the temp file
    cli.TASKS_FILE = str(fp)

    cli.add_task("Title A", "Description A", None)
    captured = capsys.readouterr()
    assert "Task added" in captured.out

    cli.list_tasks()
    out = capsys.readouterr().out
    assert "Title A" in out

def test_link_and_complete(tmp_path):
    fp = tmp_path / "tasks.json"
    cli.TASKS_FILE = str(fp)

    # add two tasks
    cli.add_task("T1", "d1", None)
    cli.add_task("T2", "d2", None)

    # link task 1 to 2
    cli.link_tasks(1, 2)
    # mark completed
    cli.complete_task(1)

    tasks = utils.read_tasks_from_file(str(fp))
    assert any(t['id'] == 1 and t.get('completed') for t in tasks)
    assert any(t['id'] == 1 and 2 in t.get('links', []) for t in tasks)
