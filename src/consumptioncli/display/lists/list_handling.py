from abc import ABC, abstractmethod
from collections.abc import Sequence
from enum import StrEnum
from typing import Any, override

from tabulate import tabulate

from consumptioncli.display.formatting import s
from consumptioncli.display.types import HasEntityProtocol

NOT_APPLICABLE = "-"


class DisplayListBase[T](ABC):
    def __init__(
        self,
        elements: Sequence[T],
        *,
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
    def order_keys(cls) -> Sequence[StrEnum]: ...

    @abstractmethod
    def _headers(self) -> Sequence[str]: ...

    @abstractmethod
    def _row(self, index: int, element: T) -> Sequence[Any]: ...

    def _footer(self) -> Sequence[Any]:
        return []

    @abstractmethod
    def _order_key_to_value(
        self, index: int, element: T, order_key: StrEnum
    ) -> Any | None: ...

    @override
    def __str__(self) -> str:
        headers = self._headers()
        rows = [
            *[self._row(i, e) for i, e in enumerate(self.elements)],
        ]
        count = len(rows)

        footer = self._footer()
        if len(footer) > 0:
            rows.append(footer)

        # TODO: Table styles
        # TODO: Fork tabulate for better footer line
        return (
            tabulate(rows, headers, floatfmt=".3g") + "\n" if count > 0 else ""
        ) + f"{count} Result{s(count)}..."


class EntityOrderKey(StrEnum):
    INDEX = "index"
    ID = "id"


class EntityList[EC: HasEntityProtocol](DisplayListBase[EC]):
    def __init__(
        self,
        entities: Sequence[EC],
        *,
        order_key: StrEnum = EntityOrderKey.INDEX,
        reverse: bool = False,
    ) -> None:
        super().__init__(
            entities,
            order_key=order_key,
            reverse=reverse,
        )

    @override
    @classmethod
    def order_keys(cls) -> Sequence[StrEnum]:
        return [EntityOrderKey.ID]

    @override
    def _headers(self) -> Sequence[str]:
        return ["#", "ID"]

    @override
    def _row(self, index: int, element: EC) -> Sequence[Any]:
        entity = element.entity
        return [index + 1, entity.id]

    @override
    def _footer(self) -> Sequence[Any]:
        return [NOT_APPLICABLE, NOT_APPLICABLE]

    @override
    def _order_key_to_value(
        self, index: int, element: EC, order_key: StrEnum
    ) -> Any | None:
        entity = element.entity
        match order_key:
            case EntityOrderKey.ID:
                return entity.id
            case _:
                return index
