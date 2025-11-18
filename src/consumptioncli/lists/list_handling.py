# stdlib
from abc import ABC, abstractmethod
from collections.abc import Sequence
from enum import StrEnum
from typing import TYPE_CHECKING, Any, Generic, TypeVar

if TYPE_CHECKING:
    from _typeshed import SupportsRichComparison

# 3rd party
from tabulate import tabulate

# consumption
from consumptionbackend.entities import EntityBase


T = TypeVar("T")


class DisplayListBase(ABC, Generic[T]):

    def __init__(
        self,
        elements: Sequence[T],
        order_key: StrEnum,
        reverse: bool = False,
    ) -> None:
        # Thanks to Andrew Clark for solution to sorting list with NoneTypes https://stackoverflow.com/a/18411610
        def sort_function(pair: tuple[int, T]):
            value = self._order_key_to_value(pair[0], pair[1], order_key)
            return (value is not None, value)

        self.elements: Sequence[T] = [
            value
            for _, value in sorted(
                enumerate(elements),
                key=sort_function,
                reverse=reverse,
            )
        ]

    @classmethod
    @abstractmethod
    def order_keys(cls) -> Sequence[StrEnum]:
        pass

    @classmethod
    @abstractmethod
    def _headers(cls) -> Sequence[str]:
        pass

    @abstractmethod
    def _row(self, index: int, element: T) -> Sequence[Any]:
        pass

    @abstractmethod
    def _order_key_to_value(
        self, index: int, element: T, order_key: StrEnum
    ) -> SupportsRichComparison | None:
        pass

    def __str__(self) -> str:
        # TODO: Average row for numeric values?
        headers = type(self)._headers()
        rows = [self._row(i, e) for i, e in enumerate(self.elements)]
        # TODO: Table styles
        # TODO: Fork tabulate for footer line
        return tabulate(rows, headers)


# TODO: 3.12 Generic handling
E = TypeVar("E", bound=EntityBase)


class EntityOrderKey(StrEnum):
    INDEX = "index"
    ID = "id"


class EntityList(DisplayListBase[E], Generic[E]):

    def __init__(
        self,
        entities: Sequence[E],
        order_key: StrEnum = EntityOrderKey.INDEX,
        reverse: bool = False,
    ) -> None:
        super().__init__(
            entities,
            order_key,
            reverse,
        )

    @classmethod
    def order_keys(cls) -> Sequence[StrEnum]:
        return [EntityOrderKey.ID]

    @classmethod
    def _headers(cls) -> Sequence[str]:
        return ["#", "ID"]

    def _row(self, index: int, element: E) -> Sequence[Any]:
        return [index + 1, element.id]

    def _order_key_to_value(
        self, index: int, element: E, order_key: StrEnum
    ) -> SupportsRichComparison | None:
        match order_key:
            case EntityOrderKey.ID:
                return element.id
            case _:
                return index
