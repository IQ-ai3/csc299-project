"""Top-level tasks3 package (src layout).

Provides a minimal `inc` function and a `main()` entrypoint that can be
called by tests or external code.
"""
from __future__ import annotations

def inc(n: int) -> int:
    """Return n + 1.

    Simple function used by tests.
    """
    return n + 1


def main() -> dict:
    """Run a tiny demo and return results.

    This function is intentionally small so CI / tests can call it without
    pulling in other packages.
    """
    return {"inc_2": inc(2), "inc_5": inc(5)}


__all__ = ["inc", "main"]
