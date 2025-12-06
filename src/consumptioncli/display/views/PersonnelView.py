from collections.abc import Sequence
from dataclasses import dataclass
from typing import override

from consumptionbackend.entities import Consumable, Personnel

from consumptioncli.display.lists import ConsumableRoleList
from consumptioncli.display.types import EntityRoles
from consumptioncli.utils import unique


@dataclass(frozen=True)
class PersonnelView:
    personnel: Personnel
    consumables: Sequence[EntityRoles[Consumable]]
    date_format: str = r"%Y/%m/%d"

    @override
    def __str__(self) -> str:
        return "\n\n".join(
            map(
                lambda x: "\n".join(x),
                [
                    self._header(self.personnel),
                    self._stats(
                        unique(
                            lambda x, y: x.id == y.id,
                            [c.entity for c in self.consumables],
                        ),
                        self.date_format,
                    ),
                    self._consumables(self.consumables),
                ],
            )
        )

    @classmethod
    def _header(cls, p: Personnel) -> Sequence[str]:
        return [f"#{p.id} {p.full_name()}"]

    @classmethod
    def _stats(cls, cs: Sequence[Consumable], date_format: str) -> Sequence[str]:
        if len(cs) == 0:
            return []

        ratings = [c.rating for c in cs if c.rating is not None]
        average_rating = sum(ratings) / len(ratings) if len(ratings) > 0 else None

        first_start_date = (
            min([c.start_date for c in cs if c.start_date is not None])
            if any([c.start_date is not None for c in cs])
            else None
        )
        final_end_date = (
            min([c.start_date for c in cs if c.start_date is not None])
            if all([c.start_date is not None for c in cs])
            else None
        )

        total_parts = sum([c.parts for c in cs])
        total_max_parts = (
            sum([c.max_parts for c in cs if c.max_parts is not None])
            if any([c.max_parts is not None for c in cs])
            else None
        )

        return [
            f"Average Rating {average_rating if average_rating is not None else '?'}",
            f"{first_start_date.strftime(date_format) if first_start_date is not None else '?'} - {final_end_date.strftime(date_format) if final_end_date is not None else '?'}",
            f"{total_parts}/{total_max_parts if total_max_parts is not None else '?'} Parts",
        ]

    @classmethod
    def _consumables(cls, c: Sequence[EntityRoles[Consumable]]) -> Sequence[str]:
        if len(c) == 0:
            return ["No Consumables assigned..."]

        return ["Consumables:", str(ConsumableRoleList(c))]
