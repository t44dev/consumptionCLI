from collections.abc import Sequence
from enum import StrEnum
from typing import Any

from consumptionbackend.database import (
    ApplyQuery,
    ConsumableApplyMapping,
    ConsumableFieldsRequired,
    ConsumableService,
    PersonnelService,
    SeriesService,
    WhereMapping,
    consumable_required_to_where,
)
from consumptionbackend.entities import Consumable, Personnel, Series
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
from consumptioncli.display.types import ConsumableContainer, EntityRole
from consumptioncli.display.views.ConsumableView import ConsumableView


class ConsumableCommandHandler:
    @classmethod
    def new(
        cls, *, force: bool, date_format: str, new: ConsumableFieldsRequired, **_: Any
    ) -> str:
        consumable_service = ServiceProvider.get(ConsumableService)

        if not force:
            existing = len(consumable_service.find(**consumable_required_to_where(new)))
            if not confirm_existing(Consumable, existing):
                return cancelled_new(Consumable)

        consumable_id = consumable_service.new(**new)
        consumable = consumable_container(
            consumable_service.find_by_id(consumable_id), include_personnel=False
        )

        consumable_view = ConsumableView(consumable, date_format=date_format)
        return str(consumable_view)

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
        consumable_service = ServiceProvider.get(ConsumableService)

        consumables = [
            consumable_container(c, include_personnel=False, include_tags=False)
            for c in consumable_service.find(**where)
        ]

        consumables_list = ConsumableList(
            consumables, order_key=order_key, reverse=reverse, date_format=date_format
        )
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

        consumable_service = ServiceProvider.get(ConsumableService)

        if not force:
            consumables = len(consumable_service.find(**where))
            if not confirm_many(consumables, update_many(Consumable, consumables)):
                return cancelled_update(Consumable)

        consumable_ids = consumable_service.update(where, apply)
        consumables = [
            consumable_container(c, include_personnel=False, include_tags=False)
            for c in consumable_service.find_by_ids(consumable_ids)
        ]

        consumables_list = ConsumableList(
            consumables, order_key=order_key, reverse=reverse, date_format=date_format
        )
        return str(consumables_list)

    @classmethod
    def delete(cls, *, force: bool, where: WhereMapping, **_: Any) -> str:
        consumable_service = ServiceProvider.get(ConsumableService)

        if not force:
            consumables = len(consumable_service.find(**where))
            if not confirm_many(consumables, delete_many(Consumable, consumables)):
                return cancelled_deletion(Consumable)

        consumables_deleted = consumable_service.delete(**where)
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
        consumable_service = ServiceProvider.get(ConsumableService)
        series_service = ServiceProvider.get(SeriesService)

        series = series_service.find(**apply)
        if len(series) == 0:
            return no_matching(Series)

        if not force:
            selected_series = select_one(series)
        else:
            selected_series = series[0]

        if selected_series is None:
            return none_selected(Series)

        consumables_ids = consumable_service.update(
            where, {"series_id": ApplyQuery(selected_series.id)}
        )
        consumables = [
            consumable_container(c, include_personnel=False, include_tags=False)
            for c in consumable_service.find_by_ids(consumables_ids)
        ]

        consumables_list = ConsumableList(
            consumables, order_key=order_key, reverse=reverse, date_format=date_format
        )
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
        consumable_service = ServiceProvider.get(ConsumableService)
        personnel_service = ServiceProvider.get(PersonnelService)

        if not force:
            consumables = len(consumable_service.find(**consumable_where))
            if not confirm_many(
                consumables, change(Personnel, Consumable, consumables)
            ):
                return cancelled_relation_update(Consumable, Personnel)

        # TODO: Just create Personnel if one doesn't exist?
        consumable_ids = consumable_service.change_personnel(
            consumable_where, personnel_where, roles
        )
        consumables = consumable_service.find_by_ids(consumable_ids)

        return "\n\n".join(
            [
                f"[{c.type}] {c.name}"
                + "\n"
                + str(
                    PersonnelRoleList(
                        [
                            EntityRole(personnel_service.find_by_id(irs.id), role)
                            for irs in consumable_service.personnel(c.id)
                            for role in irs.roles
                        ]
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
        consumable_service = ServiceProvider.get(ConsumableService)

        consumables = consumable_service.find(**where)
        if len(consumables) == 0:
            return no_matching(Consumable)

        selected_consumable = select_one(consumables) if not force else consumables[0]
        if selected_consumable is None:
            return none_selected(Consumable)

        consumable = consumable_container(selected_consumable)

        consumable_view = ConsumableView(consumable, date_format)
        return str(consumable_view)


def consumable_container(
    consumable: Consumable,
    *,
    include_series: bool = True,
    include_personnel: bool = True,
    include_tags: bool = True,
) -> ConsumableContainer:
    consumable_service = ServiceProvider.get(ConsumableService)
    personnel_service = ServiceProvider.get(PersonnelService)

    return ConsumableContainer(
        consumable,
        consumable_service.series(consumable.id) if include_series else None,
        [
            EntityRole(personnel_service.find_by_id(irs.id), role)
            for irs in consumable_service.personnel(consumable.id)
            for role in irs.roles
        ]
        if include_personnel
        else None,
        consumable_service.tags(consumable.id) if include_tags else None,
    )
