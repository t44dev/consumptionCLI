from collections.abc import Sequence
from enum import StrEnum
from typing import Any, cast

from consumptionbackend.database import (
    ApplyQuery,
    ConsumableApplyMapping,
    ConsumableFieldsRequired,
    ConsumableWhereMapping,
    WhereMapping,
    WhereQuery,
)

from consumptioncli.lists import ConsumableList, PersonnelRoleList
from consumptioncli.lists.PersonnelList import PersonnelRoles
from consumptioncli.utils import confirm_action, s

from .database import ConsumableHandler, PersonnelHandler, SeriesHandler


class ConsumableCommandHandler:
    @classmethod
    def new(
        cls, *, force: bool, date_format: str, new: ConsumableFieldsRequired, **_: Any
    ) -> str:
        if not force:
            where: ConsumableWhereMapping = cast(
                ConsumableWhereMapping,
                cast(object, {k: [WhereQuery(v)] for k, v in new.items()}),
            )
            existing = len(ConsumableHandler.find(consumables=where))
            if existing > 0:
                print(f"{existing} similar Consumable{s(existing)} found.")
                if not confirm_action("creation"):
                    return "Consumable creation cancelled."

        consumable_id = ConsumableHandler.new(**new)
        consumable = ConsumableHandler.find_by_id(consumable_id)

        consumables_list = ConsumableList([consumable], date_format=date_format)
        return str(consumables_list)

    @classmethod
    def list(
        cls,
        *,
        date_format: str,
        order_key: StrEnum,
        reverse: bool,
        where: WhereMapping,
        **_: Any,
    ) -> str:
        consumables = ConsumableHandler.find(**where)

        consumables_list = ConsumableList(consumables, order_key, reverse, date_format)
        return str(consumables_list)

    @classmethod
    def update(
        cls,
        *,
        force: bool,
        date_format: str,
        order_key: StrEnum,
        reverse: bool,
        where: WhereMapping,
        apply: ConsumableApplyMapping,
        **_: Any,
    ) -> str:
        if len(apply) == 0:
            return "No updates specified."

        if not force:
            consumables = len(ConsumableHandler.find(**where))
            if consumables > 1 and not confirm_action(
                f"update of {consumables} Consumables"
            ):
                return "Consumable update cancelled."

        # TODO: What happens if none are found
        consumable_ids = ConsumableHandler.update(where, apply)
        consumables = ConsumableHandler.find_by_ids(consumable_ids)

        consumables_list = ConsumableList(consumables, order_key, reverse, date_format)
        return str(consumables_list)

    @classmethod
    def delete(cls, *, force: bool, where: WhereMapping, **_: Any) -> str:
        if not force:
            existing = len(ConsumableHandler.find(**where))
            if existing > 1:
                print(f"{existing} Consumable{s(existing)} found.")
                if not confirm_action("deletion"):
                    return "Consumable deletion cancelled."

        consumables_deleted = ConsumableHandler.delete(**where)
        return f"{consumables_deleted} Consumables deleted."

    @classmethod
    def series(
        cls,
        *,
        force: bool,
        date_format: str,
        order_key: StrEnum,
        reverse: bool,
        where: WhereMapping,
        apply: WhereMapping,
        **_: Any,
    ) -> str:
        existing_series = SeriesHandler.find(**apply)
        selected_series = None

        if not force and len(existing_series) > 1:
            print(f"{len(existing_series)} matched Series.")
            for series in existing_series:
                if confirm_action(f"usage of [{series.id}] {series.name}"):
                    selected_series = series
                    break

            if selected_series is None:
                return "No Series selected."

        selected_series = existing_series[0] if selected_series is None else selected_series
        consumables_ids = ConsumableHandler.update(
            where, {"series_id": ApplyQuery(selected_series.id)}
        )
        consuambles = ConsumableHandler.find_by_ids(consumables_ids)

        consumables_list = ConsumableList(consuambles, order_key, reverse, date_format)
        return str(consumables_list)

    @classmethod
    def personnel(
        cls,
        *,
        force: bool,
        consumable_where: WhereMapping,
        personnel_where: WhereMapping,
        roles: Sequence[ApplyQuery[str]],
        **_: Any,
    ) -> str:
        if not force:
            consumables = len(ConsumableHandler.find(**consumable_where))
            if consumables > 1 and not confirm_action(
                f"change of Personnel for {consumables} Consumables"
            ):
                return "Consumable Personnel update cancelled."

        # TODO: Just create Personnel if one doesn't exist?
        consumable_ids = ConsumableHandler.change_personnel(
            consumable_where, personnel_where, roles
        )
        consumables = ConsumableHandler.find_by_ids(consumable_ids)

        return "\n\n".join(
            [
                f"[{c.type}] {c.name}"
                + "\n"
                + str(
                    PersonnelRoleList(
                        list(
                            map(
                                lambda er: PersonnelRoles(
                                    PersonnelHandler.find_by_id(er.id), er.roles
                                ),
                                ConsumableHandler.personnel(c.id),
                            )
                        ),
                    )
                )
                for c in consumables
            ]
        )


# TODO: View command
