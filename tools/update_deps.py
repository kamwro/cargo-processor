#!/usr/bin/env python3
"""
Upgrade or freeze Python dependencies for the cargo service.

Usage:
  cargo tools/update_deps.py --file requirements.txt            # upgrade each top-level spec to latest and rewrite file
  cargo tools/update_deps.py --file requirements.txt --freeze-only  # only pin currently installed versions

Behavior:
- Reads the given requirements file and collects top-level package names
  (ignores comments, blank lines, and constraint markers).
- If not --freeze-only, upgrades those names to latest with `pip install -U`.
- Writes back requirements.txt with exact versions for the original top-level names
  based on the currently installed environment (via `pip show`).

This script operates on the CURRENT interpreter environment. It's recommended
to run it inside your virtualenv. See cargo/Makefile targets for convenience.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable, List, Set


PKG_RE = re.compile(r"^\s*([A-Za-z0-9_.-]+)")


def read_top_level_names(req_path: Path) -> List[str]:
    names: List[str] = []
    seen: Set[str] = set()
    for line in req_path.read_text().splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("-") or s.startswith("git+"):
            continue
        m = PKG_RE.match(s)
        if not m:
            continue
        name = m.group(1)
        if name.lower() not in seen:
            names.append(name)
            seen.add(name.lower())
    return names


def pip(*args: str) -> int:
    cmd = [sys.executable, "-m", "pip", *args]
    print("$", " ".join(cmd))
    return subprocess.call(cmd)


def get_installed_version(name: str) -> str | None:
    try:
        out = subprocess.check_output([sys.executable, "-m", "pip", "show", name], text=True)
    except subprocess.CalledProcessError:
        return None
    for line in out.splitlines():
        if line.lower().startswith("version:"):
            return line.split(":", 1)[1].strip()
    return None


def rewrite_requirements(req_path: Path, names: Iterable[str]) -> None:
    lines: List[str] = []
    for n in names:
        v = get_installed_version(n)
        if not v:
            print(f"Warning: {n} not installed; skipping pin")
            continue
        lines.append(f"{n}=={v}")
    content = "\n".join(lines) + "\n"
    req_path.write_text(content)
    print(f"Wrote {req_path} with {len(lines)} pinned packages")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default="requirements.txt", help="requirements file to update")
    ap.add_argument("--freeze-only", action="store_true", help="do not upgrade, only pin what's installed")
    args = ap.parse_args()

    req_path = Path(args.file).resolve()
    if not req_path.exists():
        print(f"Requirements file not found: {req_path}", file=sys.stderr)
        return 2

    names = read_top_level_names(req_path)
    if not names:
        print("No top-level packages detected in requirements file. Nothing to do.")
        return 0

    if not args.freeze_only:
        # Upgrade each name to latest available version
        rc = pip("install", "--upgrade", *names)
        if rc != 0:
            print("pip upgrade failed; aborting", file=sys.stderr)
            return rc

    # Pin versions back to requirements.txt
    rewrite_requirements(req_path, names)
    return 0


if __name__ == "__main__":
    sys.exit(main())
