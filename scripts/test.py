#!/usr/bin/env python3
"""Run pytest (forwards all extra args)."""

from __future__ import annotations

import subprocess
import sys


def main() -> int:
    cmd = [sys.executable, "-m", "pytest", *sys.argv[1:]]
    print("$", " ".join(cmd))
    return subprocess.run(cmd).returncode


if __name__ == "__main__":
    raise SystemExit(main())
