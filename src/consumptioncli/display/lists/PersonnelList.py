from collections.abc import Sequence
from enum import StrEnum
from typing import Any, final, override

from consumptionbackend.entities import Consumable, Personnel

from consumptioncli.display.formatting import truncate
from consumptioncli.display.stats import average_rating
from consumptioncli.display.types import EntityRole, PersonnelContainer

from .list_handling import NOT_APPLICABLE, EntityList


class PersonnelOrderKey(StrEnum):
    NAME = "name"
    APPEARANCES = "appearances"
    RATING = "rating"


@final
class PersonnelList(EntityList[PersonnelContainer]):
    def __init__(
        self,
        personnel: Sequence[PersonnelContainer],
        *,
        order_key: StrEnum = PersonnelOrderKey.RATING,
        reverse: bool = False,
    ) -> None:
        super().__init__(
            personnel,
            order_key=order_key,
            reverse=reverse,
        )

    @override
    @classmethod
    def order_keys(cls) -> Sequence[StrEnum]:
        return [*super().order_keys(), *list(PersonnelOrderKey)]

    @override
    def _headers(self) -> Sequence[str]:
        headers = [*super()._headers(), "Name"]

        if all([p.consumables is not None for p in self.elements]):
            headers.extend(["Appearances", "Average Rating"])

        return headers

    @override
    def _row(self, index: int, element: PersonnelContainer) -> Sequence[Any]:
        personnel = element.entity

        row = [*super()._row(index, element), personnel.full_name()]

        unique_consumables = element.unique_consumables()
        if unique_consumables is not None:
            row.extend([len(unique_consumables), average_rating(unique_consumables)])

        return row

    @override
    def _footer(self) -> Sequence[Any]:
        footer = [*super()._footer(), NOT_APPLICABLE]

        if all([p.consumables is not None for p in self.elements]):
            unique_consumables = [p.unique_consumables() for p in self.elements]
            appearances = sum([len(uq) for uq in unique_consumables if uq is not None])
            average_ratings = [
                r
                for r in [
                    average_rating(uc) for uc in unique_consumables if uc is not None
                ]
                if r is not None
            ]
            average_average_ratings = (
                (sum(average_ratings) / len(average_ratings))
                if len(average_ratings) > 0
                else None
            )

            footer.extend([appearances, average_average_ratings])

        return footer

    @override
    def _order_key_to_value(
        self, index: int, element: PersonnelContainer, order_key: StrEnum
    ) -> Any | None:
        personnel = element.entity
        unique_consumables = element.unique_consumables()

        match order_key:
            case PersonnelOrderKey.NAME:
                return personnel.full_name()
            case PersonnelOrderKey.APPEARANCES:
                if unique_consumables is not None:
                    return len(unique_consumables)
            case PersonnelOrderKey.RATING:
                if unique_consumables is not None:
                    return average_rating(unique_consumables)
            case _:
                return super()._order_key_to_value(index, element, order_key)


class PersonnelRoleOrderKey(StrEnum):
    NAME = "name"
    ROLE = "role"


@final
class PersonnelRoleList(EntityList[EntityRole[Personnel]]):
    def __init__(
        self,
        personnel_roles: Sequence[EntityRole[Personnel]],
        *,
        order_key: StrEnum = PersonnelRoleOrderKey.NAME,
        reverse: bool = False,
    ) -> None:
        super().__init__(
            personnel_roles,
            order_key=order_key,
            reverse=reverse,
        )

    @override
    @classmethod
    def order_keys(cls) -> Sequence[StrEnum]:
        return [*super().order_keys(), *list(PersonnelRoleOrderKey)]

    @override
    def _headers(self) -> Sequence[str]:
        return [*super()._headers(), "Name", "Role"]

    @override
    def _row(self, index: int, element: EntityRole[Personnel]) -> Sequence[Any]:
        personnel = element.entity
        role = element.role
        return [
            *super()._row(index, element),
            truncate(personnel.full_name()),
            truncate(role),
        ]

    @override
    def _order_key_to_value(
        self, index: int, element: EntityRole[Personnel], order_key: StrEnum
    ) -> Any | None:
        personnel = element.entity
        role = element.role
        match order_key:
            case PersonnelRoleOrderKey.NAME:
                return personnel.full_name()
            case PersonnelRoleOrderKey.ROLE:
                return role
            case _:
                return index


class ConsumableRoleOrderKey(StrEnum):
    TYPE = "type"
    NAME = "name"
    ROLE = "role"


@final
class ConsumableRoleList(EntityList[EntityRole[Consumable]]):
    def __init__(
        self,
        consumable_roles: Sequence[EntityRole[Consumable]],
        *,
        order_key: StrEnum = ConsumableRoleOrderKey.NAME,
        reverse: bool = False,
    ) -> None:
        super().__init__(
            consumable_roles,
            order_key=order_key,
            reverse=reverse,
        )

    @override
    @classmethod
    def order_keys(cls) -> Sequence[StrEnum]:
        return [*super().order_keys(), *list(ConsumableRoleOrderKey)]

    @override
    def _headers(self) -> Sequence[str]:
        return [*super()._headers(), "Type", "Name", "Role"]

    @override
    def _row(self, index: int, element: EntityRole[Consumable]) -> Sequence[Any]:
        consumable = element.entity
        role = element.role
        return [
            *super()._row(index, element),
            consumable.type,
            truncate(consumable.name),
            truncate(role),
        ]

    @override
    def _order_key_to_value(
        self, index: int, element: EntityRole[Consumable], order_key: StrEnum
    ) -> Any | None:
        consumable = element.entity
        role = element.role
        match order_key:
            case ConsumableRoleOrderKey.TYPE:
                return consumable.type
            case ConsumableRoleOrderKey.NAME:
                return consumable.name
            case ConsumableRoleOrderKey.ROLE:
                return role
            case _:
                return index
