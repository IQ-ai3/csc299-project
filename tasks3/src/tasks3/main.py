"""Small CLI/entrypoint for the tasks3 package.

This module exposes a `main()` function so the package can be executed as
`python -m tasks3` or run directly. It delegates to `tasks3.main()`.
"""
from __future__ import annotations

from . import main as _main_fn


def main() -> None:
    """Run the package demo and print results to stdout."""
    results = _main_fn()
    # Pretty-print a simple key/value list
    for key, value in results.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
