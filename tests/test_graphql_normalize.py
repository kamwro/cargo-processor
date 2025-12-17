import json

from fastapi.testclient import TestClient

from app.api import create_app


def client() -> TestClient:
    return TestClient(create_app())


def test_graphql_normalize_basic():
    c = client()
    query = (
        "mutation($src:String!, $p: JSON!){ "
        "normalize(source:$src, payload:$p){ "
        "itemTypes{ name unitWeightKg unitVolumeM3 } "
        "items{ itemTypeName quantity } "
        "} }"
    )

    payload = {
        "types": [
            {"name": "Box S", "unitWeightKg": 1.0, "unitVolumeM3": 0.02},
            {"name": "Box M", "unitWeightKg": 2.0, "unitVolumeM3": 0.05},
        ],
        "items": [
            {"type": "Box S", "q": 3},
            {"type": "Box M", "q": 1},
        ],
    }

    body = {"query": query, "variables": {"src": "test", "p": payload}}
    r = c.post("/graphql", data=json.dumps(body), headers={"Content-Type": "application/json"})
    assert r.status_code == 200
    data = r.json()
    assert "errors" not in data
    out = data["data"]["normalize"]
    # Ensure two types and two items returned with expected fields
    assert len(out["itemTypes"]) == 2
    assert {t["name"] for t in out["itemTypes"]} == {"Box S", "Box M"}
    assert len(out["items"]) == 2
    assert out["items"][0]["quantity"] >= 0


def test_graphql_normalize_empty_payload():
    c = client()
    query = (
        "mutation($src:String!, $p: JSON!){ "
        "normalize(source:$src, payload:$p){ "
        "itemTypes{ name unitWeightKg unitVolumeM3 } "
        "items{ itemTypeName quantity } "
        "} }"
    )

    body = {"query": query, "variables": {"src": "test", "p": {}}}
    r = c.post("/graphql", data=json.dumps(body), headers={"Content-Type": "application/json"})
    assert r.status_code == 200
    data = r.json()
    assert "errors" not in data
    out = data["data"]["normalize"]
    assert out["itemTypes"] == []
    assert out["items"] == []
