#!/usr/bin/env python3
"""Run uvicorn for local dev (reload by default; supports --workers/--no-reload)."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys



def main() -> int:
    parser = argparse.ArgumentParser(description="Run uvicorn for local dev")
    parser.add_argument("--host", default=os.environ.get("HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", 8000)))
    parser.add_argument("--workers", type=int, default=0, help="Number of workers (0 means single with reload)")
    parser.add_argument("--no-reload", action="store_true", help="Disable auto-reload")
    args = parser.parse_args()

    base = [sys.executable, "-m", "uvicorn", "main:app", "--host", args.host, "--port", str(args.port)]

    if args.workers and args.workers > 0:
        base += ["--workers", str(args.workers)]
    else:
        if not args.no_reload:
            base += ["--reload"]

    print("$", " ".join(base))
    return subprocess.run(base).returncode


if __name__ == "__main__":
    raise SystemExit(main())
