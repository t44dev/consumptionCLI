from collections.abc import Sequence
from dataclasses import dataclass
from typing import override

from consumptionbackend.entities import Consumable, Personnel, Series

from consumptioncli.display.lists import PersonnelRoleList
from consumptioncli.display.types import EntityRoles


@dataclass(frozen=True)
class ConsumableView:
    consumable: Consumable
    series: Series
    personnel: Sequence[EntityRoles[Personnel]]
    date_format: str = r"%Y/%m/%d"

    @override
    def __str__(self) -> str:
        return "\n\n".join(
            map(
                lambda x: "\n".join(x),
                [
                    self._header(self.consumable, self.series),
                    self._stats(self.consumable, self.date_format),
                    self._personnel(self.personnel),
                ],
            )
        )

    @classmethod
    def _header(cls, c: Consumable, s: Series) -> Sequence[str]:
        return [
            f"#{c.id} [{c.type}] {c.name}",
            f"Series: {s.name}",
        ]

    @classmethod
    def _stats(cls, c: Consumable, date_format: str) -> Sequence[str]:
        sections = [
            f"{f'Rated {c.rating} - ' if c.rating is not None else ''}{c.completions} Completions",
        ]

        if c.start_date is not None:
            sections.append(
                f"{c.start_date.strftime(date_format)} - {c.end_date.strftime(date_format) if c.end_date else '?'}"
            )

        sections.append(
            f"{c.status} - {c.parts}/{c.max_parts if c.max_parts is not None else '?'} Parts"
        )

        return sections

    @classmethod
    def _personnel(cls, p: Sequence[EntityRoles[Personnel]]) -> Sequence[str]:
        if len(p) == 0:
            return ["No Personnel assigned..."]

        return ["Personnel:", str(PersonnelRoleList(p))]
