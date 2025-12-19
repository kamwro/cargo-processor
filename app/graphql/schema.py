from typing import Any, Annotated, cast

import strawberry
from strawberry.scalars import JSON
from strawberry.types import Info

from .resolvers import normalize_payload


@strawberry.input
class ItemTypeIn:
    name: str
    unitWeightKg: float
    unitVolumeM3: float
    lengthM: float | None = None
    widthM: float | None = None
    heightM: float | None = None


@strawberry.input
class ItemIn:
    itemTypeName: str
    quantity: int


@strawberry.type
class ItemType:
    name: str
    unitWeightKg: float
    unitVolumeM3: float
    lengthM: float | None = None
    widthM: float | None = None
    heightM: float | None = None


@strawberry.type
class Item:
    itemTypeName: str
    quantity: int


@strawberry.type
class NormalizeResult:
    itemTypes: list[ItemType]
    items: list[Item]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def normalize(self, info: Info, source: str, payload: Annotated[Any, JSON]) -> NormalizeResult:
        # mypy: JSON is a runtime scalar (Any); cast to dict for downstream function
        payload_dict = cast(dict[str, Any], payload or {})
        return normalize_payload(source=source, payload=payload_dict)


@strawberry.type
class Query:
    @strawberry.field
    def health(self) -> str:
        return "ok"


schema = strawberry.Schema(query=Query, mutation=Mutation)
