from collections.abc import Sequence
from enum import StrEnum
from typing import Any, final, override

from consumptioncli.constants import DEFAULT_DATE_FORMAT
from consumptioncli.display.formatting import q, truncate
from consumptioncli.display.stats import (
    average_rating,
    global_end_date,
    global_start_date,
    total_max_parts,
    total_parts,
)
from consumptioncli.display.types import SeriesContainer

from .list_handling import NOT_APPLICABLE, EntityList


class SeriesOrderKey(StrEnum):
    NAME = "name"
    ENTRIES = "entries"
    RATING = "rating"
    PARTS = "parts"
    MAX_PARTS = "parts"
    COMPLETIONS = "completions"
    STARTED = "started"
    COMPLETED = "completed"


@final
class SeriesList(EntityList[SeriesContainer]):
    def __init__(
        self,
        series: Sequence[SeriesContainer],
        *,
        order_key: StrEnum = SeriesOrderKey.RATING,
        reverse: bool = False,
        date_format: str = DEFAULT_DATE_FORMAT,
    ) -> None:
        super().__init__(
            series,
            order_key=order_key,
            reverse=reverse,
        )
        self.date_format = date_format

    @override
    @classmethod
    def order_keys(cls) -> Sequence[StrEnum]:
        return [*super().order_keys(), *list(SeriesOrderKey)]

    @override
    def _headers(self) -> Sequence[str]:
        headers = [*super()._headers(), "Name"]

        if all([s.consumables is not None for s in self.elements]):
            headers.extend(
                [
                    "Entries",
                    "Average Rating",
                    "Parts",
                    "Completions",
                    "Started",
                    "Completed",
                ]
            )

        return headers

    @override
    def _row(self, index: int, element: SeriesContainer) -> Sequence[Any]:
        series = element.entity

        row = [*super()._row(index, element), truncate(series.name)]

        if element.consumables is not None:
            rating = average_rating(element.consumables)
            parts = total_parts(element.consumables)
            max_parts = total_max_parts(element.consumables)
            start_date = global_start_date(element.consumables)
            end_date = global_end_date(element.consumables)

            row.extend(
                [
                    len(element.consumables),
                    rating,
                    f"{parts}/{q(max_parts)}",
                    sum([c.completions for c in element.consumables]),
                    start_date.strftime(self.date_format)
                    if start_date is not None
                    else "",
                    end_date.strftime(self.date_format) if end_date is not None else "",
                ]
            )

        return row

    @override
    def _footer(self) -> Sequence[Any]:
        footer = [*super()._footer(), NOT_APPLICABLE]

        if all([s.consumables is not None for s in self.elements]):
            consumables = [
                c
                for s in self.elements
                if s.consumables is not None
                for c in s.consumables
            ]
            parts = total_parts(consumables)
            max_parts = total_max_parts(consumables)
            average_ratings = average_rating(consumables)
            completions = sum([c.completions for c in consumables])

            footer.extend(
                [
                    NOT_APPLICABLE,
                    average_ratings,
                    f"{parts}/{q(max_parts)}",
                    completions,
                    NOT_APPLICABLE,
                    NOT_APPLICABLE,
                ]
            )

        return footer

    @override
    def _order_key_to_value(
        self, index: int, element: SeriesContainer, order_key: StrEnum
    ) -> Any | None:
        series = element.entity

        match order_key:
            case SeriesOrderKey.NAME:
                return series.name
            case SeriesOrderKey.ENTRIES:
                if element.consumables is not None:
                    return len(element.consumables)
            case SeriesOrderKey.RATING:
                if element.consumables is not None:
                    return average_rating(element.consumables)
            case SeriesOrderKey.PARTS:
                if element.consumables is not None:
                    return total_parts(element.consumables)
            case SeriesOrderKey.MAX_PARTS:
                if element.consumables is not None:
                    return total_max_parts(element.consumables)
            case SeriesOrderKey.COMPLETIONS:
                if element.consumables is not None:
                    return sum([c.completions for c in element.consumables])
            case SeriesOrderKey.STARTED:
                if element.consumables is not None:
                    return global_start_date(element.consumables)
            case SeriesOrderKey.COMPLETED:
                if element.consumables is not None:
                    return global_end_date(element.consumables)
            case _:
                return super()._order_key_to_value(index, element, order_key)
