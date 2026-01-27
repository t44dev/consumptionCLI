from collections.abc import Sequence
from dataclasses import dataclass
from typing import override

from consumptionbackend.entities import Consumable, Series

from consumptioncli.constants import DEFAULT_DATE_FORMAT
from consumptioncli.display.formatting import q
from consumptioncli.display.lists import ConsumableList
from consumptioncli.display.stats import (
    average_rating,
    global_end_date,
    global_start_date,
    total_max_parts,
    total_parts,
)
from consumptioncli.display.types import ConsumableContainer, SeriesContainer


@dataclass(frozen=True)
class SeriesView:
    series: SeriesContainer
    date_format: str = DEFAULT_DATE_FORMAT

    @override
    def __str__(self) -> str:
        rows = [self._header(self.series.entity)]

        if self.series.consumables:
            rows.append(self._stats(self.series.consumables, self.date_format))

        return "\n\n".join(map(lambda x: "\n".join(x), rows))

    @classmethod
    def _header(cls, s: Series) -> Sequence[str]:
        return [f"#{s.id} {s.name}"]

    @classmethod
    def _stats(cls, cs: Sequence[Consumable], date_format: str) -> Sequence[str]:
        if len(cs) == 0:
            return []

        rating = average_rating(cs)
        parts = total_parts(cs)
        max_parts = total_max_parts(cs)
        start_date = global_start_date(cs)
        end_date = global_end_date(cs)

        return [
            f"Average Rating {q(rating)}",
            f"{parts}/{q(max_parts)} Parts",
            f"{q(start_date, lambda x: x.strftime(date_format))} - {q(end_date, lambda x: x.strftime(date_format))}",
        ]

    @classmethod
    def _consumables(cls, cs: Sequence[Consumable], date_format: str) -> Sequence[str]:
        if len(cs) == 0:
            return ["No Consumables assigned..."]

        return [
            "Consumables:",
            str(
                ConsumableList(
                    list(map(lambda x: ConsumableContainer(x), cs)),
                    date_format=date_format,
                )
            ),
        ]
