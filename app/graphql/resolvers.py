from typing import Any

from ..services.normalizer import normalize_raw
from .types import Item, ItemType, NormalizeResult


def normalize_payload(source: str, payload: dict[str, Any]) -> NormalizeResult:
    item_types, items = normalize_raw(source, payload)
    return NormalizeResult(
        itemTypes=[ItemType(**it) for it in item_types],
        items=[Item(**i) for i in items],
    )
