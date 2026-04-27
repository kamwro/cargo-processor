# cargo-processor

A FastAPI + Strawberry GraphQL microservice that normalizes raw cargo payload data (field aliasing, type coercion, default values) and returns a structured result.

## Architecture

```
HTTP POST /graphql
  → FastAPI (app/api.py · create_app)
  → CORS middleware
  → API key auth (app/core/security.py · require_api_key)
  → Strawberry GraphQL router
    → Mutation.normalize (app/graphql/schema.py)
    → normalize_payload resolver (app/graphql/resolvers.py)
    → normalize_raw service (app/services/normalizer.py)
    → NormalizeResult (app/graphql/types.py)
```

## Key conventions

- **All Strawberry types** (input + output) live in `app/graphql/types.py`.
- **All intra-package imports** within `app/graphql/` use relative imports (`from .types import ...`).
- **Settings** are a Pydantic `BaseSettings` singleton accessed via `get_settings()` (`app/core/config.py`).
- **Field alias mapping** in the normalizer uses `_get(obj, *keys, default=..., cast=...)` — add new mappings there.
- **JSON scalar** in `schema.py` uses a `TYPE_CHECKING` guard — do not remove it.

## Dev commands

```bash
python scripts/run.py          # start Uvicorn dev server (localhost:8000)
python scripts/test.py         # run pytest
python scripts/lint.py         # ruff check
python scripts/typecheck.py    # mypy strict
python scripts/build.py        # syntax check + optional Docker build
```

## Test strategy

- `tests/conftest.py` — shared `client: TestClient` pytest fixture (always use this, never instantiate `TestClient` directly in test files)
- `tests/test_services_normalizer.py` — unit tests for `normalize_raw()`
- `tests/test_graphql_normalize.py` — integration tests via GraphQL mutation
- `tests/test_health_ready.py` — health/ready endpoint tests

GraphQL test pattern:
```python
body = {"query": "mutation(...){ normalize(...){ ... } }", "variables": {...}}
r = client.post("/graphql", data=json.dumps(body), headers={"Content-Type": "application/json"})
assert "errors" not in r.json()
```

## Environment variables

| Variable          | Default | Description                          |
|-------------------|---------|--------------------------------------|
| `API_KEY`         | —       | Required auth key (dev: skip if unset) |
| `LOG_LEVEL`       | `INFO`  | Python logging level                  |
| `ALLOWED_ORIGINS` | `[]`    | CSV list of allowed CORS origins      |

Copy `.env.example` → `.env` to configure locally.

## GraphQL API

```graphql
mutation Normalize($source: String!, $payload: JSON!) {
  normalize(source: $source, payload: $payload) {
    itemTypes { name unitWeightKg unitVolumeM3 lengthM widthM heightM }
    items { itemTypeName quantity }
  }
}
```

Auth header: `X-Cargo-Api-Key: <API_KEY>`

## Adding a new field mapping

1. Add the field to `_get(...)` calls in `app/services/normalizer.py` inside `normalize_raw()`
2. Add it to the corresponding Strawberry type in `app/graphql/types.py`
3. Add a test case in `tests/test_services_normalizer.py`
4. Run `python scripts/test.py && python scripts/typecheck.py`
