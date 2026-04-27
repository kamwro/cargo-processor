from typing import Any, Callable, TypeVar

_T = TypeVar("_T")


def _get(obj: dict[str, Any], *keys: str, default: _T, cast: Callable[[Any], _T]) -> _T:
    for key in keys:
        val = obj.get(key)
        if val is not None:
            return cast(val)
    return default


def normalize_raw(source: str, raw: dict[str, Any]) -> tuple[list[dict], list[dict]]:
    types_raw = raw.get("types") or []
    items_raw = raw.get("items") or []

    item_types: list[dict] = []
    items: list[dict] = []

    for t in types_raw:
        item_types.append(
            {
                "name": _get(t, "name", "id", default="Unknown", cast=str),
                "unitWeightKg": _get(t, "unitWeightKg", "w", default=0.0, cast=float),
                "unitVolumeM3": _get(t, "unitVolumeM3", "v", default=0.0, cast=float),
                "lengthM": float(t["lengthM"]) if t.get("lengthM") is not None else None,
                "widthM": float(t["widthM"]) if t.get("widthM") is not None else None,
                "heightM": float(t["heightM"]) if t.get("heightM") is not None else None,
            }
        )

    for it in items_raw:
        items.append(
            {
                "itemTypeName": _get(it, "itemTypeName", "type", default="Unknown", cast=str),
                "quantity": _get(it, "quantity", "q", default=0, cast=int),
            }
        )

    return item_types, items
