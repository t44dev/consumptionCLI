# stdlib
from collections.abc import Sequence
from typing import cast, final
from itertools import chain

# 3rd party
from tabulate import tabulate

# consumable
from consumptionbackend.entities import Personnel
from .list_handling import EntityListBase


@final
class PersonnelList(EntityListBase):

    COLUMN_HEADERS: Sequence[str] = list(
        chain(
            EntityListBase.DEFAULT_HEADERS,
            [
                "Name",
            ],
        )
    )

    def __init__(self, entities: Sequence[Personnel]) -> None:
        super().__init__(entities)

    def __str__(self) -> str:
        # TODO: Consumable data i.e. average rating
        rows = [
            [
                i + 1,
                p.id,
                " ".join(
                    cast(
                        filter[str],
                        filter(
                            lambda name: name is not None,
                            [
                                p.first_name,
                                f'"{p.pseudonym}"' if p.pseudonym is not None else None,
                                p.last_name,
                            ],
                        ),
                    )
                ),
            ]
            for i, p in enumerate(cast(Sequence[Personnel], self._entities))
        ]
        return tabulate(rows, PersonnelList.COLUMN_HEADERS)
