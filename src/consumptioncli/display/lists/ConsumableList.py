from collections.abc import Sequence
from enum import StrEnum
from typing import Any, final, override

from consumptioncli.constants import DEFAULT_DATE_FORMAT
from consumptioncli.display.formatting import q, truncate
from consumptioncli.display.types import ConsumableContainer

from .list_handling import EntityList


class ConsumableOrderKey(StrEnum):
    TYPE = "type"
    SERIES = "series"
    NAME = "name"
    PARTS = "parts"
    MAX_PARTS = "max_parts"
    RATING = "rating"
    COMPLETIONS = "completions"
    STATUS = "status"
    STARTED = "started"
    COMPLETED = "completed"


@final
class ConsumableList(EntityList[ConsumableContainer]):
    def __init__(
        self,
        consumables: Sequence[ConsumableContainer],
        *,
        order_key: StrEnum = ConsumableOrderKey.RATING,
        reverse: bool = False,
        date_format: str = DEFAULT_DATE_FORMAT,
    ) -> None:
        super().__init__(
            consumables,
            order_key=order_key,
            reverse=reverse,
        )
        self.date_format = date_format

    @override
    @classmethod
    def order_keys(cls) -> Sequence[StrEnum]:
        return [*super().order_keys(), *list(ConsumableOrderKey)]

    @override
    def _headers(self) -> Sequence[str]:
        headers = [*super()._headers(), "Type"]

        if any([c.series is not None for c in self.elements]):
            headers.append("Series")

        headers.extend([
            "Name",
            "Parts",
            "Rating",
            "Completions",
            "Status",
            "Started",
            "Completed",
        ])

        return headers

    @override
    def _row(self, index: int, element: ConsumableContainer) -> Sequence[Any]:
        consumable = element.entity
        row = [*super()._row(index, element), consumable.type]

        if element.series is not None:
            row.append(truncate(element.series.name))

        return [
            *row,
            truncate(consumable.name),
            f"{consumable.parts}/{q(consumable.max_parts)}",
            consumable.rating,
            consumable.completions,
            str(consumable.status),
            consumable.start_date.strftime(self.date_format)
            if consumable.start_date is not None
            else "",
            consumable.end_date.strftime(self.date_format)
            if consumable.end_date is not None
            else "",
        ]

    @override
    def _order_key_to_value(
        self, index: int, element: ConsumableContainer, order_key: StrEnum
    ) -> Any | None:
        consumable = element.entity
        match order_key:
            case ConsumableOrderKey.TYPE:
                return consumable.type
            case ConsumableOrderKey.SERIES:
                if element.series is not None:
                    return element.series.name
            case ConsumableOrderKey.NAME:
                return consumable.name
            case ConsumableOrderKey.PARTS:
                return consumable.parts
            case ConsumableOrderKey.MAX_PARTS:
                return consumable.max_parts
            case ConsumableOrderKey.RATING:
                return consumable.rating
            case ConsumableOrderKey.COMPLETIONS:
                return consumable.completions
            case ConsumableOrderKey.STATUS:
                return consumable.status
            case ConsumableOrderKey.STARTED:
                return consumable.start_date
            case ConsumableOrderKey.COMPLETED:
                return consumable.end_date
            case _:
                return super()._order_key_to_value(index, element, order_key)
