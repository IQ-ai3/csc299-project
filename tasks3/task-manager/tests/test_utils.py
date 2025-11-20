import sys
import pathlib

# Ensure src directory is importable
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

import utils

def test_generate_unique_id_empty():
    assert utils.generate_unique_id([]) == 1

def test_read_write(tmp_path):
    fp = tmp_path / "tasks.json"
    tasks = [{"id": 1, "title": "t", "description": "d", "links": [], "completed": False}]
    utils.write_tasks_to_file(str(fp), tasks)
    loaded = utils.read_tasks_from_file(str(fp))
    assert loaded == tasks
