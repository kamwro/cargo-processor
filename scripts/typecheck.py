#!/usr/bin/env python3
"""Run mypy type checks (use --strict for stricter mode; supports extra args after --)."""

from __future__ import annotations

import argparse
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Run mypy type checks")
    parser.add_argument("paths", nargs="*", default=["."], help="Paths to check (default: .)")
    parser.add_argument("--strict", action="store_true", help="Enable mypy --strict")
    parser.add_argument("--", dest="extra", nargs=argparse.REMAINDER, help="Extra args passed to mypy")
    args = parser.parse_args()

    cmd = [sys.executable, "-m", "mypy", *args.paths]
    if args.strict:
        cmd.append("--strict")
    else:
        # Friendly defaults for repos without full typing yet
        cmd += [
            "--ignore-missing-imports",
            "--warn-unused-ignores",
            "--no-warn-no-return",
        ]
    if args.extra:
        cmd += args.extra

    print("$", " ".join(cmd))
    return subprocess.run(cmd).returncode


if __name__ == "__main__":
    raise SystemExit(main())
