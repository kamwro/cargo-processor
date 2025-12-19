from typing import TYPE_CHECKING, Any, cast

import strawberry
from strawberry.scalars import JSON as JSONScalar
from strawberry.types import Info

from .resolvers import normalize_payload
from app.graphql.types import NormalizeResult


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


# Output types are defined in app/graphql/types.py to avoid circular imports

# Use Strawberry's JSON scalar at runtime while keeping type-checkers happy
if TYPE_CHECKING:
    # Accept any JSON-like structure at type-check time
    JSONInput = Any
else:
    JSONInput = JSONScalar


@strawberry.type
class Mutation:
    @strawberry.mutation
    def normalize(self, info: Info, source: str, payload: JSONInput) -> NormalizeResult:
        # mypy: JSON is a runtime scalar (Any); cast to dict for downstream function
        payload_dict = cast(dict[str, Any], payload or {})
        return normalize_payload(source=source, payload=payload_dict)


@strawberry.type
class Query:
    @strawberry.field
    def health(self) -> str:
        return "ok"


schema = strawberry.Schema(query=Query, mutation=Mutation)
