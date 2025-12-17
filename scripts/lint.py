#!/usr/bin/env python3
"""Run ruff lint (add --fix to apply safe autofixes)."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path



def run(cmd: list[str]) -> int:
    print("$", " ".join(cmd))
    return subprocess.run(cmd).returncode



def main() -> int:
    parser = argparse.ArgumentParser(description="Run ruff on the repo")
    parser.add_argument("paths", nargs="*", default=["."], help="Paths to lint (default: .)")
    parser.add_argument("--fix", action="store_true", help="Apply autofixes (ruff --fix)")
    args = parser.parse_args()

    # Ensure we're in repo
    if not (Path.cwd() / "README.md").exists():
        print("Warning: README.md not found in CWD — are you in the repo root?", file=sys.stderr)

    cmd = [sys.executable, "-m", "ruff", "check", *args.paths]
    if args.fix:
        cmd.append("--fix")

    return run(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
