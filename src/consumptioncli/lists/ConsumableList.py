from collections.abc import Sequence
from enum import StrEnum
from typing import Any, final, override

from consumptionbackend.entities import Consumable

from consumptioncli.utils import truncate

from .list_handling import EntityList


class ConsumableOrderKey(StrEnum):
    TYPE = "type"
    NAME = "name"
    PARTS = "parts"
    MAX_PARTS = "max_parts"
    RATING = "rating"
    COMPLETIONS = "completions"
    STATUS = "status"
    STARTED = "started"
    COMPLETED = "completed"


@final
class ConsumableList(EntityList[Consumable]):
    def __init__(
        self,
        entities: Sequence[Consumable],
        order_key: StrEnum = ConsumableOrderKey.RATING,
        reverse: bool = False,
        date_format: str = r"%Y/%m/%d",
    ) -> None:
        super().__init__(
            entities,
            order_key,
            reverse,
        )
        self.date_format = date_format

    @override
    @classmethod
    def order_keys(cls) -> Sequence[StrEnum]:
        return [*super().order_keys(), *list(ConsumableOrderKey)]

    @override
    @classmethod
    def _headers(cls) -> Sequence[str]:
        return [
            *super()._headers(),
            "Type",
            "Name",
            "Parts",
            "Rating",
            "Completions",
            "Status",
            "Started",
            "Completed",
        ]

    @override
    def _row(self, index: int, element: Consumable) -> Sequence[Any]:
        return [
            *super()._row(index, element),
            element.type,
            truncate(element.name),
            f"{element.parts}/{element.max_parts if element.max_parts is not None else '?'}",
            element.rating,
            element.completions,
            element.status.name.replace("_", " "),
            element.end_date.strftime(self.date_format) if element.end_date else "",
            element.end_date.strftime(self.date_format) if element.end_date else "",
        ]

    @override
    def _order_key_to_value(
        self, index: int, element: Consumable, order_key: StrEnum
    ) -> Any | None:
        match order_key:
            case ConsumableOrderKey.TYPE:
                return element.type
            case ConsumableOrderKey.NAME:
                return element.name
            case ConsumableOrderKey.PARTS:
                return element.parts
            case ConsumableOrderKey.MAX_PARTS:
                return element.max_parts
            case ConsumableOrderKey.RATING:
                return element.rating
            case ConsumableOrderKey.COMPLETIONS:
                return element.completions
            case ConsumableOrderKey.STATUS:
                return element.status
            case ConsumableOrderKey.STARTED:
                return element.start_date
            case ConsumableOrderKey.COMPLETED:
                return element.end_date
            case _:
                return super()._order_key_to_value(index, element, order_key)
