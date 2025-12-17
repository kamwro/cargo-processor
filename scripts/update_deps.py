#!/usr/bin/env python3
"""Update or freeze deps from a requirements file (default upgrade; use --freeze-only to just pin)."""

from __future__ import annotations

import argparse
from collections.abc import Iterable
from pathlib import Path
import re
import subprocess
import sys

PKG_RE = re.compile(r"^\s*([A-Za-z0-9_.-]+)")


def read_top_level_names(req_path: Path) -> list[str]:
    names: list[str] = []
    seen: set[str] = set()
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
    lines: list[str] = []
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
