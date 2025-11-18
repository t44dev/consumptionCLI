# consumption
from collections.abc import Sequence
from enum import StrEnum
from consumptionbackend.database import (
    ApplyQuery,
    ConsumableFieldsRequired,
    ConsumableApplyMapping,
    WhereMapping,
)
from consumptionbackend.database.sqlite import SeriesHandler
from consumptioncli.lists import ConsumableList, PersonnelRoleList
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
        consumable = ConsumableHandler.new(**args["new"])
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
        consumables = ConsumableHandler.update(args["where"], args["apply"])
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
        # TODO: How do we know how many are deleted?
        ConsumableHandler.delete(**args["where"])
        return "Done"

    @classmethod
    def series(cls, args: ConsumableSeriesCommandArguments) -> str:
        # TODO: Confirm series for multiple hits
        series = SeriesHandler.find(**args["apply"])
        series_id = series[0].id
        consumables = ConsumableHandler.update(
            args["where"], {"series_id": ApplyQuery(series_id)}
        )
        consumables_list = ConsumableList(
            consumables,
            args["order_key"],
            args["reverse"],
            args["date_format"],
        )
        return str(consumables_list)

    @classmethod
    def personnel(cls, args: ConsumableChangePersonnelCommandArguments) -> str:
        # TODO: Can we just create personnel if they don't exist?
        consumable_personnel = ConsumableHandler.change_personnel(
            args["consumable_where"], args["personnel_where"], args["roles"]
        )

        return "\n\n".join(
            [
                cp.consumable.name + "\n" + str(PersonnelRoleList(cp.personnel))
                for cp in consumable_personnel
            ]
        )


# TODO: View command
