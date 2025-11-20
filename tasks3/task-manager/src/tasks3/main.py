"""CLI entrypoint for tasks3 (inside task-manager/src/tasks3).

Delegates to the package-level main() function so `python -m tasks3`
or the console script work when the package is located under
`task-manager/src/tasks3`.
"""
from __future__ import annotations

from . import main as _main_fn


def main() -> None:
    results = _main_fn()
    for k, v in results.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
