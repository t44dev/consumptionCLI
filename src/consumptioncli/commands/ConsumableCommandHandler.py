from collections.abc import Sequence
from enum import StrEnum

from consumptionbackend.database import (
    ApplyQuery,
    ConsumableApplyMapping,
    ConsumableFieldsRequired,
    WhereMapping,
)
from consumptionbackend.database.sqlite import PersonnelHandler, SeriesHandler

from consumptioncli.lists import ConsumableList, PersonnelRoleList
from consumptioncli.lists.PersonnelList import PersonnelRoles

from .command_handling import CommandArgumentsBase, WhereArguments
from .database import ConsumableHandler


class ConsumableNewCommandArguments(CommandArgumentsBase):
    new: ConsumableFieldsRequired


class ConsumableListCommandArguments(WhereArguments):
    order_key: StrEnum
    reverse: bool


class ConsumableUpdateCommandArguments(WhereArguments):
    apply: ConsumableApplyMapping
    order_key: StrEnum
    reverse: bool


class ConsumableSeriesCommandArguments(WhereArguments):
    apply: WhereMapping
    order_key: StrEnum
    reverse: bool


class ConsumableChangePersonnelCommandArguments(CommandArgumentsBase):
    consumable_where: WhereMapping
    personnel_where: WhereMapping
    roles: Sequence[ApplyQuery[str]]


class ConsumableCommandHandler:
    @classmethod
    def new(cls, args: ConsumableNewCommandArguments) -> str:
        # TODO: Can we do a check to see if something similar already exists?
        consumable_id = ConsumableHandler.new(**args["new"])
        consumable = ConsumableHandler.find_by_id(consumable_id)

        consumables_list = ConsumableList(
            [consumable],
            date_format=args["date_format"],
        )
        return str(consumables_list)

    @classmethod
    def list(cls, args: ConsumableListCommandArguments) -> str:
        consumables = ConsumableHandler.find(**args["where"])

        consumables_list = ConsumableList(
            consumables,
            args["order_key"],
            args["reverse"],
            args["date_format"],
        )
        return str(consumables_list)

    @classmethod
    def update(cls, args: ConsumableUpdateCommandArguments) -> str:
        # TODO: What if no values to set are provided?
        # TODO: Confirm update for multiple hits
        # TODO: What happens if none are found
        # TODO: Tagging
        consumable_ids = ConsumableHandler.update(args["where"], args["apply"])
        consumables = ConsumableHandler.find_by_ids(consumable_ids)

        consumables_list = ConsumableList(
            consumables,
            args["order_key"],
            args["reverse"],
            args["date_format"],
        )
        return str(consumables_list)

    @classmethod
    def delete(cls, args: WhereArguments) -> str:
        # TODO: Confirm delete for multiple hits
        consumables_deleted = ConsumableHandler.delete(**args["where"])
        return f"{consumables_deleted} Consumables deleted."

    @classmethod
    def series(cls, args: ConsumableSeriesCommandArguments) -> str:
        # TODO: Confirm series for multiple hits
        series = SeriesHandler.find(**args["apply"])
        series_id = series[0].id
        consumables_ids = ConsumableHandler.update(
            args["where"], {"series_id": ApplyQuery(series_id)}
        )
        consuambles = ConsumableHandler.find_by_ids(consumables_ids)

        consumables_list = ConsumableList(
            consuambles,
            args["order_key"],
            args["reverse"],
            args["date_format"],
        )
        return str(consumables_list)

    @classmethod
    def personnel(cls, args: ConsumableChangePersonnelCommandArguments) -> str:
        # TODO: Can we just create personnel if they don't exist?
        consumable_ids = ConsumableHandler.change_personnel(
            args["consumable_where"], args["personnel_where"], args["roles"]
        )
        consumables = ConsumableHandler.find_by_ids(consumable_ids)

        return "\n\n".join(
            [
                c.name
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
                        )
                    )
                )
                for c in consumables
            ]
        )


# TODO: View command
