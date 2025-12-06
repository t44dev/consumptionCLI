from enum import StrEnum
from typing import Any

from consumptionbackend.database import (
    PersonnelApplyMapping,
    PersonnelFieldsRequired,
    WhereMapping,
    personnel_required_to_where,
)
from consumptionbackend.entities import Personnel

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
from consumptioncli.display.types import EntityRoles
from consumptioncli.display.views import PersonnelView

from .database import ConsumableHandler, PersonnelHandler


class PersonnelCommandHandler:
    @classmethod
    def new(cls, *, force: bool, new: PersonnelFieldsRequired, **_: Any) -> str:
        if not force:
            existing = len(PersonnelHandler.find(*personnel_required_to_where(new)))
            if not confirm_existing(Personnel, existing):
                return cancelled_new(Personnel)

        personnel_id = PersonnelHandler.new(**new)
        personnel = PersonnelHandler.find_by_id(personnel_id)

        personnel_list = PersonnelList([personnel])
        return str(personnel_list)

    @classmethod
    def list(
        cls, *, order_key: StrEnum, reverse: bool, where: WhereMapping, **_: Any
    ) -> str:
        personnel = PersonnelHandler.find(**where)

        personnel_list = PersonnelList(personnel, order_key, reverse)
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

        if not force:
            personnel = len(PersonnelHandler.find(**where))
            if not confirm_many(personnel, update_many(Personnel, personnel)):
                return cancelled_update(Personnel)

        personnel_ids = PersonnelHandler.update(where, apply)
        personnel = PersonnelHandler.find_by_ids(personnel_ids)

        personnel_list = PersonnelList(personnel, order_key, reverse)
        return str(personnel_list)

    @classmethod
    def delete(cls, *, force: bool, where: WhereMapping, **_: Any) -> str:
        if not force:
            personnel = len(PersonnelHandler.find(**where))
            if not confirm_many(personnel, delete_many(Personnel, personnel)):
                return cancelled_deletion(Personnel)

        personnel_deleted = PersonnelHandler.delete(**where)
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
        personnel = PersonnelHandler.find(**where)
        if len(personnel) == 0:
            return no_matching(Personnel)

        if not force:
            selected_personnel = select_one(personnel)
        else:
            selected_personnel = personnel[0]

        if selected_personnel is None:
            return none_selected(Personnel)

        personnel = list(
            map(
                lambda ir: EntityRoles(ConsumableHandler.find_by_id(ir.id), ir.roles),
                PersonnelHandler.consumables(selected_personnel.id),
            )
        )

        return str(PersonnelView(selected_personnel, personnel, date_format))
