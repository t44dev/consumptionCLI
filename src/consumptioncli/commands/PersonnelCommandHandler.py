from enum import StrEnum
from typing import Any

from consumptionbackend.database import (
    ConsumableService,
    PersonnelApplyMapping,
    PersonnelFieldsRequired,
    PersonnelService,
    WhereMapping,
    personnel_required_to_where,
)
from consumptionbackend.entities import Personnel
from consumptionbackend.utils import ServiceProvider

from consumptioncli.commands.input import (
    confirm_existing,
    confirm_many,
    select_one,
)
from consumptioncli.commands.messages import (
    NO_UPDATES,
    cancelled_deletion,
    cancelled_new,
    cancelled_update,
    delete_many,
    deleted,
    no_matching,
    none_selected,
    update_many,
)
from consumptioncli.display.lists import PersonnelList
from consumptioncli.display.types import EntityRole, PersonnelContainer
from consumptioncli.display.views import PersonnelView


class PersonnelCommandHandler:
    @classmethod
    def new(
        cls, *, force: bool, date_format: str, new: PersonnelFieldsRequired, **_: Any
    ) -> str:
        personnel_service = ServiceProvider.get(PersonnelService)

        if not force:
            existing = len(personnel_service.find(**personnel_required_to_where(new)))
            if not confirm_existing(Personnel, existing):
                return cancelled_new(Personnel)

        personnel_id = personnel_service.new(**new)
        personnel = personnel_container(
            personnel_service.find_by_id(personnel_id), include_consumables=False
        )

        personnel_view = PersonnelView(personnel, date_format=date_format)
        return str(personnel_view)

    @classmethod
    def list(
        cls, *, order_key: StrEnum, reverse: bool, where: WhereMapping, **_: Any
    ) -> str:
        personnel_service = ServiceProvider.get(PersonnelService)

        personnel = [personnel_container(p) for p in personnel_service.find(**where)]

        personnel_list = PersonnelList(personnel, order_key=order_key, reverse=reverse)
        return str(personnel_list)

    @classmethod
    def update(
        cls,
        *,
        force: bool,
        order_key: StrEnum,
        reverse: bool,
        where: WhereMapping,
        apply: PersonnelApplyMapping,
        **_: Any,
    ) -> str:
        if len(apply) == 0:
            return NO_UPDATES

        personnel_service = ServiceProvider.get(PersonnelService)

        if not force:
            personnel = len(personnel_service.find(**where))
            if not confirm_many(personnel, update_many(Personnel, personnel)):
                return cancelled_update(Personnel)

        personnel_ids = personnel_service.update(where, apply)
        personnel = [
            personnel_container(p) for p in personnel_service.find_by_ids(personnel_ids)
        ]

        personnel_list = PersonnelList(personnel, order_key=order_key, reverse=reverse)
        return str(personnel_list)

    @classmethod
    def delete(cls, *, force: bool, where: WhereMapping, **_: Any) -> str:
        personnel_service = ServiceProvider.get(PersonnelService)

        if not force:
            personnel = len(personnel_service.find(**where))
            if not confirm_many(personnel, delete_many(Personnel, personnel)):
                return cancelled_deletion(Personnel)

        personnel_deleted = personnel_service.delete(**where)
        return deleted(Personnel, personnel_deleted)

    @classmethod
    def view(
        cls,
        *,
        force: bool,
        date_format: str,
        where: WhereMapping,
        **_: Any,
    ) -> str:
        personnel_service = ServiceProvider.get(PersonnelService)

        personnel = personnel_service.find(**where)
        if len(personnel) == 0:
            return no_matching(Personnel)

        selected_personnel = select_one(personnel) if not force else personnel[0]

        if selected_personnel is None:
            return none_selected(Personnel)

        personnel = personnel_container(selected_personnel)

        personnel_view = PersonnelView(personnel, date_format)
        return str(personnel_view)


def personnel_container(
    personnel: Personnel, *, include_consumables: bool = True
) -> PersonnelContainer:
    personnel_service = ServiceProvider.get(PersonnelService)
    consumable_service = ServiceProvider.get(ConsumableService)

    return PersonnelContainer(
        personnel,
        [
            EntityRole(consumable_service.find_by_id(irs.id), role)
            for irs in personnel_service.consumables(personnel.id)
            for role in irs.roles
        ]
        if include_consumables
        else None,
    )
