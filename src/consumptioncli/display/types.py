from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

from consumptionbackend.entities import Consumable, EntityBase, Personnel, Series

from consumptioncli.utils import unique


class HasEntityProtocol(Protocol):
    @property
    def entity(self) -> EntityBase: ...


@dataclass(frozen=True)
class EntityContainer[E: EntityBase]:
    entity: E


@dataclass(frozen=True)
class EntityRole[E: EntityBase](EntityContainer[E]):
    role: str


@dataclass(frozen=True)
class ConsumableContainer(EntityContainer[Consumable]):
    series: Series | None = None
    personnel: Sequence[EntityRole[Personnel]] | None = None
    tags: Sequence[str] | None = None


@dataclass(frozen=True)
class PersonnelContainer(EntityContainer[Personnel]):
    consumables: Sequence[EntityRole[Consumable]] | None = None

    def unique_consumables(self) -> Sequence[Consumable] | None:
        return (
            unique(lambda x, y: x.id == y.id, [er.entity for er in self.consumables])
            if self.consumables is not None
            else None
        )


@dataclass(frozen=True)
class SeriesContainer(EntityContainer[Series]):
    consumables: Sequence[Consumable] | None = None


@dataclass(frozen=True)
class TagContainer:
    tag: str
    consumables: Sequence[Consumable] | None = None
