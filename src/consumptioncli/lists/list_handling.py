# stdlib
from abc import ABC, abstractmethod
from collections.abc import MutableSequence, Sequence

# consumption
from consumptionbackend.entities import EntityBase


class EntityListBase(ABC):

    DEFAULT_HEADERS: Sequence[str] = ["#", "ID"]
    COLUMN_HEADERS: Sequence[str]

    def __init__(self, entities: Sequence[EntityBase]) -> None:
        super().__init__()
        self._entities: MutableSequence[EntityBase] = [entity for entity in entities]

    def sort(self, key: str, reverse: bool = False) -> None:
        # Thanks to Andrew Clark for solution to sorting list with NoneTypes https://stackoverflow.com/a/18411610
        self._entities = sorted(
            self._entities,
            key=lambda a: (getattr(a, key) is not None, getattr(a, key)),
            reverse=reverse,
        )

    @abstractmethod
    def __str__(self) -> str:
        return super().__str__()
