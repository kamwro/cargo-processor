import strawberry
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
    def normalize(self, info: Info, source: str, payload: strawberry.scalars.JSON) -> NormalizeResult:
        return normalize_payload(source=source, payload=payload or {})


schema = strawberry.Schema(mutation=Mutation)
