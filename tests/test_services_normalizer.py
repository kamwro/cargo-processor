from app.services.normalizer import normalize_raw


def test_normalize_raw_maps_fields_and_defaults():
    src = "unit"
    raw = {
        "types": [
            {"id": "S", "w": 1, "v": 0.02},
            {"name": "Box M", "unitWeightKg": 2.5, "unitVolumeM3": 0.05, "lengthM": 0.6},
        ],
        "items": [
            {"type": "S", "q": 3},
            {"itemTypeName": "Box M", "quantity": 2},
            {},  # defaults
        ],
    }

    item_types, items = normalize_raw(src, raw)

    # Validate types mapping
    assert len(item_types) == 2
    t0 = item_types[0]
    assert t0["name"] == "S"
    assert t0["unitWeightKg"] == 1.0
    assert t0["unitVolumeM3"] == 0.02
    assert t0["lengthM"] is None and t0["widthM"] is None and t0["heightM"] is None

    t1 = item_types[1]
    assert t1["name"] == "Box M"
    assert t1["lengthM"] == 0.6

    # Validate items mapping and defaults
    assert len(items) == 3
    assert items[0] == {"itemTypeName": "S", "quantity": 3}
    assert items[1] == {"itemTypeName": "Box M", "quantity": 2}
    assert items[2] == {"itemTypeName": "Unknown", "quantity": 0}
