from collections.abc import Sequence
from enum import StrEnum
from typing import Any, NamedTuple, final, override

from consumptionbackend.entities import Personnel

from consumptioncli.utils import truncate

from .list_handling import DisplayListBase, EntityList


class PersonnelOrderKey(StrEnum):
    NAME = "name"


@final
class PersonnelList(EntityList[Personnel]):
    def __init__(
        self,
        entities: Sequence[Personnel],
        order_key: StrEnum = PersonnelOrderKey.NAME,
        reverse: bool = False,
    ) -> None:
        super().__init__(
            entities,
            order_key,
            reverse,
        )

    @override
    @classmethod
    def order_keys(cls) -> Sequence[StrEnum]:
        return [*super().order_keys(), *list(PersonnelOrderKey)]

    @override
    @classmethod
    def _headers(cls) -> Sequence[str]:
        return [*super()._headers(), "Name"]

    @override
    def _row(self, index: int, element: Personnel) -> Sequence[Any]:
        # TODO: Consumable data i.e. average rating
        return [*super()._row(index, element), element.full_name()]

    @override
    def _order_key_to_value(
        self, index: int, element: Personnel, order_key: StrEnum
    ) -> Any | None:
        match order_key:
            case PersonnelOrderKey.NAME:
                return element.full_name()
            case _:
                return super()._order_key_to_value(index, element, order_key)


class PersonnelRoleOrderKey(StrEnum):
    NAME = "name"
    ROLE = "role"


class PersonnelRoles(NamedTuple):
    personnel: Personnel
    roles: Sequence[str]


@final
class PersonnelRoleList(DisplayListBase[tuple[Personnel, str]]):
    def __init__(
        self,
        entities: Sequence[PersonnelRoles],
        order_key: StrEnum = PersonnelRoleOrderKey.NAME,
        reverse: bool = False,
    ) -> None:
        super().__init__(
            [(pr.personnel, role) for pr in entities for role in pr.roles],
            order_key,
            reverse,
        )

    @override
    @classmethod
    def order_keys(cls) -> Sequence[StrEnum]:
        return list(PersonnelRoleOrderKey)

    @override
    @classmethod
    def _headers(cls) -> Sequence[str]:
        return ["Name", "Role"]

    @override
    def _row(self, index: int, element: tuple[Personnel, str]) -> Sequence[Any]:
        # TODO: Consumable data i.e. average rating
        return [truncate(element[0].full_name()), truncate(element[1])]

    @override
    def _order_key_to_value(
        self, index: int, element: tuple[Personnel, str], order_key: StrEnum
    ) -> Any | None:
        match order_key:
            case PersonnelRoleOrderKey.NAME:
                return element[0].full_name()
            case PersonnelRoleOrderKey.ROLE:
                return element[1]
            case _:
                return index
