from collections.abc import Sequence
from dataclasses import dataclass
from typing import override

from consumptionbackend.entities import Consumable, Personnel, Series

from consumptioncli.constants import DEFAULT_DATE_FORMAT
from consumptioncli.display.formatting import q
from consumptioncli.display.lists import PersonnelRoleList
from consumptioncli.display.types import ConsumableContainer, EntityRole


@dataclass(frozen=True)
class ConsumableView:
    consumable: ConsumableContainer
    date_format: str = DEFAULT_DATE_FORMAT

    @override
    def __str__(self) -> str:
        rows = [
            self._header(self.consumable.entity, self.consumable.series),
            self._stats(self.consumable.entity, self.date_format),
        ]

        if self.consumable.tags is not None:
            rows.append(self._tags(self.consumable.tags))

        if self.consumable.personnel is not None:
            rows.append(self._personnel(self.consumable.personnel))

        return "\n\n".join(map(lambda x: "\n".join(x), rows))

    @classmethod
    def _header(cls, c: Consumable, s: Series | None) -> Sequence[str]:
        header = [
            f"#{c.id} [{c.type}] {c.name}",
        ]

        if s is not None:
            header.append(f"Series: {s.name}")

        return header

    @classmethod
    def _stats(cls, c: Consumable, date_format: str) -> Sequence[str]:
        sections = [
            f"{f'Rated {c.rating} - ' if c.rating is not None else ''}{c.completions} Completions",
            f"{c.start_date.strftime(date_format)} - {q(c.end_date, lambda x: x.strftime(date_format))}"
            if c.start_date is not None
            else None,
            f"{c.status} - {c.parts}/{q(c.max_parts)} Parts",
        ]

        return [section for section in sections if section is not None]

    @classmethod
    def _tags(cls, tags: Sequence[str]) -> Sequence[str]:
        if len(tags) == 0:
            return ["No tags..."]

        return [f"Tags: {', '.join(tags)}"]

    @classmethod
    def _personnel(cls, p: Sequence[EntityRole[Personnel]]) -> Sequence[str]:
        if len(p) == 0:
            return ["No Personnel assigned..."]

        return ["Personnel:", str(PersonnelRoleList(p))]
