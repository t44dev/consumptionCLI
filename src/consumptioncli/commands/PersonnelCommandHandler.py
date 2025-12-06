from enum import StrEnum
from typing import Any, cast

from consumptionbackend.database import (
    PersonnelApplyMapping,
    PersonnelFieldsRequired,
    PersonnelWhereMapping,
    WhereMapping,
    WhereQuery,
)

from consumptioncli.display.lists import PersonnelList
from consumptioncli.display.types import EntityRoles
from consumptioncli.display.views import PersonnelView
from consumptioncli.utils import confirm_action

from .database import ConsumableHandler, PersonnelHandler


class PersonnelCommandHandler:
    @classmethod
    def new(cls, *, force: bool, new: PersonnelFieldsRequired, **_: Any) -> str:
        if not force:
            where: PersonnelWhereMapping = cast(
                PersonnelWhereMapping,
                cast(object, {k: [WhereQuery(v)] for k, v in new.items()}),
            )
            existing = len(PersonnelHandler.find(personnel=where))
            if existing > 0:
                print(f"{existing} similar Personnel found.")
                if not confirm_action("creation"):
                    return "Personnel creation cancelled."

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
            return "No updates specified."

        if not force:
            personnel = len(PersonnelHandler.find(**where))
            if personnel > 1 and not confirm_action(f"update of {personnel} Personnel"):
                return "Personnel update cancelled."

        # TODO: What happens if none are found
        personnel_ids = PersonnelHandler.update(where, apply)
        personnel = PersonnelHandler.find_by_ids(personnel_ids)

        personnel_list = PersonnelList(personnel, order_key, reverse)
        return str(personnel_list)

    @classmethod
    def delete(cls, *, force: bool, where: WhereMapping, **_: Any) -> str:
        if not force:
            existing = len(PersonnelHandler.find(**where))
            if existing > 1:
                print(f"{existing} Personnel found.")
                if not confirm_action("deletion"):
                    return "Personnel deletion cancelled."

        personnel_deleted = PersonnelHandler.delete(**where)
        return f"{personnel_deleted} Personnel deleted."

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
            return "No matching Personnel."

        selected_personnel = None
        if not force and len(personnel) > 1:
            print(f"{len(personnel)} matched Personnel.")
            for p in personnel:
                if confirm_action(f"viewing {p.full_name()}"):
                    selected_personnel = p
                    break

            if selected_personnel is None:
                return "No Personnel selected."

        selected_personnel = (
            personnel[0] if selected_personnel is None else selected_personnel
        )

        consumables = list(
            map(
                lambda ir: EntityRoles(ConsumableHandler.find_by_id(ir.id), ir.roles),
                PersonnelHandler.consumables(selected_personnel.id),
            )
        )

        return str(PersonnelView(selected_personnel, consumables, date_format))
