Run the full quality check pipeline for cargo-processor in this order:

1. `python scripts/lint.py` — ruff linting (style + import order)
2. `python scripts/typecheck.py` — mypy strict type checking on `app/`
3. `python scripts/test.py` — pytest test suite

Run each step sequentially. Report the output of each step. Stop and report the failure if any step exits with a non-zero code.
