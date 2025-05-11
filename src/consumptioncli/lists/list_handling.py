# stdlib
from abc import ABC, abstractmethod
from collections.abc import MutableSequence, Sequence
from typing import Any

# consumption
from consumptionbackend.entities import EntityBase


class DisplayListBase(ABC):

    COLUMN_HEADERS: Sequence[str]

    def __init__(self, elements: Sequence[Any]) -> None:
        super().__init__()
        self._elements: MutableSequence[EntityBase] = [element for element in elements]

    def sort(self, key: str, reverse: bool = False) -> None:
        # Thanks to Andrew Clark for solution to sorting list with NoneTypes https://stackoverflow.com/a/18411610
        self._elements = sorted(
            self._elements,
            key=lambda a: (getattr(a, key) is not None, getattr(a, key)),
            reverse=reverse,
        )

    @abstractmethod
    def __str__(self) -> str:
        return super().__str__()


class EntityListBase(DisplayListBase, ABC):

    DEFAULT_HEADERS: Sequence[str] = ["#", "ID"]

    def __init__(self, entities: Sequence[EntityBase]) -> None:
        super().__init__(entities)
