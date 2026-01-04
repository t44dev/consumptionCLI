from collections.abc import Sequence
from dataclasses import dataclass
from typing import override

from consumptionbackend.entities import Consumable, Personnel

from consumptioncli.constants import DEFAULT_DATE_FORMAT
from consumptioncli.display.formatting import q
from consumptioncli.display.lists import ConsumableRoleList
from consumptioncli.display.stats import (
    average_rating,
    global_end_date,
    global_start_date,
    total_max_parts,
    total_parts,
)
from consumptioncli.display.types import EntityRole, PersonnelContainer


@dataclass(frozen=True)
class PersonnelView:
    personnel: PersonnelContainer
    date_format: str = DEFAULT_DATE_FORMAT

    @override
    def __str__(self) -> str:
        rows = [self._header(self.personnel.entity)]

        if self.personnel.consumables is not None:
            rows.append(
                self._stats(
                    self.personnel.unique_consumables(),
                    self.date_format,
                )
            )

            rows.append(self._consumables(self.personnel.consumables))

        return "\n\n".join(map(lambda x: "\n".join(x), rows))

    @classmethod
    def _header(cls, p: Personnel) -> Sequence[str]:
        return [f"#{p.id} {p.full_name()}"]

    @classmethod
    def _stats(cls, cs: Sequence[Consumable] | None, date_format: str) -> Sequence[str]:
        if cs is None or len(cs) == 0:
            return []

        rating = average_rating(cs)
        start_date = global_start_date(cs)
        end_date = global_end_date(cs)
        parts = total_parts(cs)
        max_parts = total_max_parts(cs)

        return [
            f"Average Rating {q(rating)}",
            f"{q(start_date, lambda x: x.strftime(date_format))} - {q(end_date, lambda x: x.strftime(date_format))}",
            f"{parts}/{q(max_parts)} Parts",
        ]

    @classmethod
    def _consumables(cls, c: Sequence[EntityRole[Consumable]]) -> Sequence[str]:
        if len(c) == 0:
            return ["No Consumables assigned..."]

        return ["Consumables:", str(ConsumableRoleList(c))]
