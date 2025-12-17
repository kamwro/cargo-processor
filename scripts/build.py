#!/usr/bin/env python3
"""Build helper: compile bytecode and optionally build a Docker image (with --docker)."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path



def run(cmd: list[str]) -> int:
    print("$", " ".join(cmd))
    return subprocess.run(cmd).returncode



def compile_repo() -> int:
    return run([sys.executable, "-m", "compileall", "-q", "."])



def docker_build(tag: str) -> int:
    # Build in repo root where Dockerfile lives
    dockerfile = Path("Dockerfile")
    if not dockerfile.exists():
        print("Dockerfile not found; skipping docker build", file=sys.stderr)
        return 0
    return run(["docker", "build", "-t", tag, "."])



def main() -> int:
    parser = argparse.ArgumentParser(description="Build project (compileall, optional docker)")
    parser.add_argument("--docker", action="store_true", help="Also build Docker image")
    parser.add_argument("--tag", default="cargo-processor:local", help="Docker tag (with --docker)")
    args = parser.parse_args()

    code = compile_repo()
    if code != 0:
        return code
    if args.docker:
        return docker_build(args.tag)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
