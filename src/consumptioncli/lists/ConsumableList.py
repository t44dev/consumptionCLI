# stdlib
from collections.abc import Sequence
from typing import cast, final
from itertools import chain

# 3rd party
from tabulate import tabulate

# consumable
from consumptionbackend.entities import Consumable
from .list_handling import EntityListBase
from consumptioncli.utils import truncate


@final
class ConsumableList(EntityListBase):

    COLUMN_HEADERS: Sequence[str] = list(
        chain(
            EntityListBase.DEFAULT_HEADERS,
            [
                "Type",
                "Name",
                "Parts",
                "Rating",
                "Completions",
                "Status",
                "Started",
                "Completed",
            ],
        )
    )

    def __init__(
        self, entities: Sequence[Consumable], date_format: str = r"%Y/%m/%d"
    ) -> None:
        super().__init__(entities)
        self.date_format = date_format

    def __str__(self) -> str:
        # TODO: Truncate using window width
        # TODO: Average row
        rows = [
            [
                i + 1,
                c.id,
                c.type,
                truncate(c.name),
                f"{c.parts}/{c.max_parts if c.max_parts is not None else '?'}",
                c.rating,
                c.completions,
                c.status.name,
                (
                    c.start_date.strftime(self.date_format)
                    if c.start_date is not None
                    else None
                ),
                (
                    c.end_date.strftime(self.date_format)
                    if c.end_date is not None
                    else None
                ),
            ]
            for i, c in enumerate(cast(Sequence[Consumable], self._elements))
        ]
        return tabulate(rows, ConsumableList.COLUMN_HEADERS)
