import subprocess
import sys
import json
import os
import tempfile

CLI_PATH = os.path.join(os.getcwd(), "src", "task_manager", "cli.py")


def run_cli(args, task_file):
    env = os.environ.copy()
    # Override TASK_FILE usage indirectly by running in temp directory
    cwd = os.path.dirname(task_file)
    result = subprocess.run([sys.executable, CLI_PATH] + args, cwd=cwd, capture_output=True, text=True)
    return result


def test_add_and_list_cli():
    tmpdir = tempfile.TemporaryDirectory()
    try:
        r_add = run_cli(["add", "Sample", "-d", "Desc", "-t", "alpha", "beta"], os.path.join(tmpdir.name, ".tasks.json"))
        assert r_add.returncode == 0
        r_list = run_cli(["list"], os.path.join(tmpdir.name, ".tasks.json"))
        assert "Sample" in r_list.stdout
    finally:
        tmpdir.cleanup()


def test_search_cli():
    tmpdir = tempfile.TemporaryDirectory()
    try:
        run_cli(["add", "Parser"], os.path.join(tmpdir.name, ".tasks.json"))
        run_cli(["add", "Docs"], os.path.join(tmpdir.name, ".tasks.json"))
        r_search = run_cli(["search", "-q", "Parser"], os.path.join(tmpdir.name, ".tasks.json"))
        assert "Parser" in r_search.stdout
    finally:
        tmpdir.cleanup()


def test_link_unlink_cli():
    tmpdir = tempfile.TemporaryDirectory()
    try:
        run_cli(["add", "A"], os.path.join(tmpdir.name, ".tasks.json"))
        run_cli(["add", "B"], os.path.join(tmpdir.name, ".tasks.json"))
        # link
        run_cli(["link", "1", "2"], os.path.join(tmpdir.name, ".tasks.json"))
        show = run_cli(["show", "1"], os.path.join(tmpdir.name, ".tasks.json"))
        assert "links: 2" in show.stdout
        # unlink
        run_cli(["unlink", "1", "2"], os.path.join(tmpdir.name, ".tasks.json"))
        show2 = run_cli(["show", "1"], os.path.join(tmpdir.name, ".tasks.json"))
        assert "links: -" in show2.stdout
    finally:
        tmpdir.cleanup()
