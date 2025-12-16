from typing import Any, List, Tuple


def normalize_raw(source: str, raw: dict[str, Any]) -> Tuple[List[dict], List[dict]]:
    types_raw = raw.get("types") or []
    items_raw = raw.get("items") or []

    item_types: List[dict] = []
    items: List[dict] = []

    for t in types_raw:
        item_types.append(
            {
                "name": str(t.get("name") or t.get("id") or "Unknown"),
                "unitWeightKg": float(t.get("unitWeightKg") or t.get("w") or 0.0),
                "unitVolumeM3": float(t.get("unitVolumeM3") or t.get("v") or 0.0),
                "lengthM": float(t["lengthM"]) if t.get("lengthM") is not None else None,
                "widthM": float(t["widthM"]) if t.get("widthM") is not None else None,
                "heightM": float(t["heightM"]) if t.get("heightM") is not None else None,
            }
        )

    for it in items_raw:
        items.append(
            {
                "itemTypeName": str(it.get("itemTypeName") or it.get("type") or "Unknown"),
                "quantity": int(it.get("quantity") or it.get("q") or 0),
            }
        )

    return item_types, items
