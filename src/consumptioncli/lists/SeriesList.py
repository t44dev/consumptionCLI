# stdlib
from collections.abc import Sequence
from typing import cast, final
from itertools import chain

# 3rd party
from tabulate import tabulate

# consumable
from consumptionbackend.entities import Series
from .list_handling import EntityListBase


@final
class SeriesList(EntityListBase):

    COLUMN_HEADERS: Sequence[str] = list(
        chain(
            EntityListBase.DEFAULT_HEADERS,
            [
                "Name",
            ],
        )
    )

    def __init__(self, entities: Sequence[Series]) -> None:
        super().__init__(entities)

    def __str__(self) -> str:
        # TODO: Truncate using window width
        # TODO: Consumable data i.e. average rating
        rows = [
            [i + 1, s.id, s.name]
            for i, s in enumerate(cast(Sequence[Series], self._elements))
        ]
        return tabulate(rows, SeriesList.COLUMN_HEADERS)
