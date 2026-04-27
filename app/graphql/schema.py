from typing import TYPE_CHECKING, Any, cast

import strawberry
from strawberry.scalars import JSON as JSONScalar
from strawberry.types import Info

from .types import NormalizeResult
from .resolvers import normalize_payload


# Use Strawberry's JSON scalar at runtime while keeping type-checkers happy
if TYPE_CHECKING:
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
