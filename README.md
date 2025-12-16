Cargo Processor (FastAPI + Strawberry GraphQL)

This service normalizes raw item data (types + items) via a GraphQL mutation and is designed to integrate with the storage-calculator backend.

Quick start
- Python 3.14+
- Install deps: `pip install -r requirements.txt`
- Copy env: `cp .env.example .env`
- Run: `uvicorn main:app --reload --port 8000`

Endpoints
- GraphQL: POST `/graphql` (GraphiQL in dev)
- Health:   GET  `/health`
- Ready:    GET  `/ready`

Auth
- Inbound header: `X-Cargo-Api-Key: <API_KEY>` (if `API_KEY` is set; otherwise allowed in dev)

Environment (.env)
- `API_KEY` — shared key for inbound requests (optional in dev)
- `API_TOKEN` — token this service uses to call your backend (if needed)
- `BACKEND_BASE_URL` — e.g., `http://localhost:3000/api`
- `ALLOWED_ORIGINS` — CSV for CORS
- `LOG_LEVEL` — default `INFO`

Clean README (service-only)

Usage examples

- Curl

```
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -H "X-Cargo-Api-Key: ${API_KEY:-dev-key}" \
  -d '{
    "query": "mutation($src:String!, $p: JSON!){ normalize(source:$src, payload:$p){ items{ itemTypeName quantity } itemTypes{ name unitWeightKg unitVolumeM3 } } }",
    "variables": { "src": "demo", "p": { "items": [ { "type": "Box S", "q": 3 } ] } }
  }'
```

- Python helper

```
set CARGO_URL=http://localhost:8000
set X_CARGO_API_KEY=dev-key
python examples/post_demo_payload.py
```

Docker

```
docker build -t cargo-processor:local .
docker run -p 8000:8000 --env-file .env cargo-processor:local
```

Local tooling (lint, test, build, typecheck, run)

- Install dev tools:

```
pip install -r requirements-dev.txt
```

- Lint (Ruff):

```
python tools/lint.py          # check only
python tools/lint.py --fix    # auto-fix where safe
```

- Tests (pytest):

```
python tools/test.py          # pass flags like: python tools/test.py -q -k name
```

- Type checking (mypy):

```
python tools/typecheck.py     # friendly defaults
python tools/typecheck.py --strict
```

- Build helpers:

```
python tools/build.py                 # compile .py -> .pyc (syntax check)
python tools/build.py --docker        # build Docker image (tag default: cargo-processor:local)
python tools/build.py --docker --tag your-tag
```

- Run dev server (uvicorn):

```
python tools/run.py                   # host=0.0.0.0 port=8000 reload on
python tools/run.py --host 127.0.0.1 --port 9000 --no-reload
python tools/run.py --workers 2       # multi-process (reload disabled)
```

Project structure

```
.
├─ app/
│  ├─ api.py                # FastAPI app factory + GraphQL router
│  ├─ core/                 # settings, logging, security
│  ├─ graphql/              # schema + resolvers
│  └─ services/             # pure business logic
├─ examples/                # small client scripts
├─ .env.example             # configuration template
├─ main.py                  # uvicorn entrypoint (imports create_app)
└─ README.md
```

ADRs

- ADR/0001_framework_fastapi.md
- ADR/0002_graphql_service.md

License

MIT
