import argparse
import json
import os
import sys
from typing import List

# Ensure package import works when script executed with arbitrary CWD
_CURR = os.path.dirname(os.path.abspath(__file__))
_PARENT = os.path.dirname(_CURR)
if _PARENT not in sys.path:
    sys.path.insert(0, _PARENT)

try:  # prefer absolute import
    from task_manager.storage import TaskRepository, VALID_STATUSES
except ImportError:  # fallback if executed directly inside package dir
    from storage import TaskRepository, VALID_STATUSES


def format_task(task: dict) -> str:
    links = ",".join(str(x) for x in task.get("links", [])) or "-"
    tags = ",".join(task.get("tags", [])) or "-"
    return (
        f"#{task['id']} [{task['status']}] {task['title']}\n"
        f"  desc: {task['description'] or '-'}\n"
        f"  tags: {tags}\n"
        f"  links: {links}\n"
        f"  created: {task['created_at']} updated: {task['updated_at']}"
    )


def cmd_add(repo: TaskRepository, args: argparse.Namespace) -> None:
    task = repo.add(args.title, args.description or "", args.status, args.tags)
    print(format_task(task))


def cmd_list(repo: TaskRepository, args: argparse.Namespace) -> None:
    tasks = repo.list()
    for t in tasks:
        print(format_task(t))
    if not tasks:
        print("(no tasks)")


def cmd_search(repo: TaskRepository, args: argparse.Namespace) -> None:
    tasks = repo.search(text=args.text or "", tag=args.tag, status=args.status)
    for t in tasks:
        print(format_task(t))
    print(f"Matched: {len(tasks)}")


def cmd_edit(repo: TaskRepository, args: argparse.Namespace) -> None:
    task = repo.edit(
        args.id,
        title=args.title,
        description=args.description,
        status=args.status,
        tags=args.tags,
    )
    print(format_task(task))


def cmd_delete(repo: TaskRepository, args: argparse.Namespace) -> None:
    if repo.delete(args.id):
        print(f"Deleted task {args.id}")
    else:
        print(f"Task {args.id} not found")


def cmd_link(repo: TaskRepository, args: argparse.Namespace) -> None:
    repo.link(args.source, args.target)
    print(f"Linked {args.source} <-> {args.target}")


def cmd_unlink(repo: TaskRepository, args: argparse.Namespace) -> None:
    repo.unlink(args.source, args.target)
    print(f"Unlinked {args.source} <-> {args.target}")


def cmd_show(repo: TaskRepository, args: argparse.Namespace) -> None:
    task = repo.get(args.id)
    if not task:
        print(f"Task {args.id} not found")
        return
    print(format_task(task))


def cmd_summary(repo: TaskRepository, args: argparse.Namespace) -> None:
    summary = repo.summary()
    print(json.dumps(summary, indent=2))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="CLI Task Manager")
    sub = p.add_subparsers(dest="command", required=True)

    pa = sub.add_parser("add", help="Add a task")
    pa.add_argument("title")
    pa.add_argument("-d", "--description")
    pa.add_argument("-s", "--status", default="open", choices=VALID_STATUSES)
    pa.add_argument("-t", "--tags", nargs="*")
    pa.set_defaults(func=cmd_add)

    pl = sub.add_parser("list", help="List all tasks")
    pl.set_defaults(func=cmd_list)

    ps = sub.add_parser("search", help="Search tasks")
    ps.add_argument("-q", "--text", help="Search text")
    ps.add_argument("-t", "--tag", help="Tag filter")
    ps.add_argument("-s", "--status", choices=VALID_STATUSES)
    ps.set_defaults(func=cmd_search)

    pe = sub.add_parser("edit", help="Edit task")
    pe.add_argument("id", type=int)
    pe.add_argument("-t", "--title")
    pe.add_argument("-d", "--description")
    pe.add_argument("-s", "--status", choices=VALID_STATUSES)
    pe.add_argument("-g", "--tags", nargs="*")
    pe.set_defaults(func=cmd_edit)

    pd = sub.add_parser("delete", help="Delete task")
    pd.add_argument("id", type=int)
    pd.set_defaults(func=cmd_delete)

    pli = sub.add_parser("link", help="Link two tasks")
    pli.add_argument("source", type=int)
    pli.add_argument("target", type=int)
    pli.set_defaults(func=cmd_link)

    pu = sub.add_parser("unlink", help="Remove link between tasks")
    pu.add_argument("source", type=int)
    pu.add_argument("target", type=int)
    pu.set_defaults(func=cmd_unlink)

    psw = sub.add_parser("show", help="Show single task")
    psw.add_argument("id", type=int)
    psw.set_defaults(func=cmd_show)

    psu = sub.add_parser("summary", help="Show status counts")
    psu.set_defaults(func=cmd_summary)

    return p


def main(argv: List[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    repo = TaskRepository()
    try:
        args.func(repo, args)
    except (ValueError, KeyError) as e:
        print(f"Error: {e}")
        raise SystemExit(1)

if __name__ == "__main__":  # pragma: no cover
    main()
