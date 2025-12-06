from collections.abc import Sequence
from enum import StrEnum
from typing import Any

from consumptionbackend.database import (
    ApplyQuery,
    ConsumableApplyMapping,
    ConsumableFieldsRequired,
    WhereMapping,
    consumable_required_to_where,
)
from consumptionbackend.entities import Consumable, Personnel, Series

from consumptioncli.commands.input import (
    confirm_existing,
    confirm_many,
    select_one,
)
from consumptioncli.commands.messages import (
    NO_UPDATES,
    cancelled_deletion,
    cancelled_new,
    cancelled_relation_update,
    cancelled_update,
    change,
    delete_many,
    deleted,
    no_matching,
    none_selected,
    update_many,
)
from consumptioncli.display.lists import (
    ConsumableList,
    PersonnelRoleList,
)
from consumptioncli.display.types import EntityRoles
from consumptioncli.display.views.ConsumableView import ConsumableView

from .database import ConsumableHandler, PersonnelHandler, SeriesHandler


class ConsumableCommandHandler:
    @classmethod
    def new(
        cls, *, force: bool, date_format: str, new: ConsumableFieldsRequired, **_: Any
    ) -> str:
        if not force:
            existing = len(ConsumableHandler.find(*consumable_required_to_where(new)))
            if not confirm_existing(Consumable, existing):
                return cancelled_new(Consumable)

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
            return NO_UPDATES

        if not force:
            consumables = len(ConsumableHandler.find(**where))
            if not confirm_many(consumables, update_many(Consumable, consumables)):
                return cancelled_update(Consumable)

        consumable_ids = ConsumableHandler.update(where, apply)
        consumables = ConsumableHandler.find_by_ids(consumable_ids)

        consumables_list = ConsumableList(consumables, order_key, reverse, date_format)
        return str(consumables_list)

    @classmethod
    def delete(cls, *, force: bool, where: WhereMapping, **_: Any) -> str:
        if not force:
            consumables = len(ConsumableHandler.find(**where))
            if not confirm_many(consumables, delete_many(Consumable, consumables)):
                return cancelled_deletion(Consumable)

        consumables_deleted = ConsumableHandler.delete(**where)
        return deleted(Consumable, consumables_deleted)

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
        series = SeriesHandler.find(**apply)
        if len(series) == 0:
            return no_matching(Series)

        if not force:
            selected_series = select_one(series)
        else:
            selected_series = series[0]

        if selected_series is None:
            return none_selected(Series)

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
            if not confirm_many(
                consumables, change(Personnel, Consumable, consumables)
            ):
                return cancelled_relation_update(Consumable, Personnel)

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
                                lambda ir: EntityRoles(
                                    PersonnelHandler.find_by_id(ir.id), ir.roles
                                ),
                                ConsumableHandler.personnel(c.id),
                            )
                        ),
                    )
                )
                for c in consumables
            ]
        )

    @classmethod
    def view(
        cls,
        *,
        force: bool,
        date_format: str,
        where: WhereMapping,
        **_: Any,
    ) -> str:
        consumables = ConsumableHandler.find(**where)
        if len(consumables) == 0:
            return no_matching(Consumable)

        if not force:
            selected_consumable = select_one(consumables)
        else:
            selected_consumable = consumables[0]

        if selected_consumable is None:
            return none_selected(Consumable)

        series = SeriesHandler.find_by_id(selected_consumable.series_id)
        personnel = list(
            map(
                lambda ir: EntityRoles(PersonnelHandler.find_by_id(ir.id), ir.roles),
                ConsumableHandler.personnel(selected_consumable.id),
            )
        )

        return str(ConsumableView(selected_consumable, series, personnel, date_format))
