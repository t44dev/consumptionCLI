# stdlib
from collections.abc import Sequence
from typing import cast, final
from itertools import chain

# 3rd party
from tabulate import tabulate

# consumable
from consumptionbackend.entities import Personnel, PersonnelRoles
from .list_handling import DisplayListBase, EntityListBase


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
            [i + 1, p.id, p.full_name()]
            for i, p in enumerate(cast(Sequence[Personnel], self._elements))
        ]
        return tabulate(rows, PersonnelList.COLUMN_HEADERS)


@final
class PersonnelRoleList(DisplayListBase):

    COLUMN_HEADERS: Sequence[str] = list(
        chain(
            EntityListBase.DEFAULT_HEADERS,
            [
                "Name",
                "Role",
            ],
        )
    )

    def __init__(self, elements: Sequence[PersonnelRoles]) -> None:
        super().__init__(elements)

    def __str__(self) -> str:
        rows = [
            [i + 1, pr.personnel.id, pr.personnel.full_name(), role]
            for i, pr in enumerate(cast(Sequence[PersonnelRoles], self._elements))
            for role in pr.roles
        ]
        return tabulate(rows, PersonnelRoleList.COLUMN_HEADERS)
