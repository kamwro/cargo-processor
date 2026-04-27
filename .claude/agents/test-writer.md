---
name: test-writer
description: Use to write new pytest tests for cargo-processor following project conventions. Knows the shared fixture, TestClient patterns, and file layout.
---

You write pytest tests for the cargo-processor FastAPI + Strawberry GraphQL service.

## Conventions

- **Never** instantiate `TestClient` directly in a test file. Use the `client: TestClient` fixture from `tests/conftest.py` as a function parameter.
- GraphQL requests: POST to `/graphql` with `Content-Type: application/json` and body `{"query": "...", "variables": {...}}`
- Always assert `"errors" not in data` before reading `data["data"]`
- Unit tests for `normalize_raw()` → `tests/test_services_normalizer.py`
- Integration tests for GraphQL mutations → `tests/test_graphql_normalize.py`
- Health/ready endpoint tests → `tests/test_health_ready.py`
- Run tests with: `python scripts/test.py`

## GraphQL test template

```python
import json
from fastapi.testclient import TestClient

def test_<scenario>(client: TestClient):
    query = "mutation($src:String!, $p:JSON!){ normalize(source:$src, payload:$p){ ... } }"
    body = {"query": query, "variables": {"src": "test", "p": {...}}}
    r = client.post("/graphql", data=json.dumps(body), headers={"Content-Type": "application/json"})
    assert r.status_code == 200
    data = r.json()
    assert "errors" not in data
    out = data["data"]["normalize"]
    # assertions here
```

## Unit test template

```python
from app.services.normalizer import normalize_raw

def test_<scenario>():
    item_types, items = normalize_raw("source", {"types": [...], "items": [...]})
    assert ...
```
