# consumption
from consumptionbackend.database import (
    ApplyQuery,
    ConsumableFieldsRequired,
    ConsumableApplyMapping,
    SeriesWhereMapping,
)
from consumptionbackend.database.sqlite import SeriesHandler
from consumptioncli.lists import ConsumableList
from .command_handling import CommandArgumentsBase, WhereArguments
from .database import ConsumableHandler


class ConsumableNewArguments(CommandArgumentsBase):
    new: ConsumableFieldsRequired


class ConsumableUpdateArguments(WhereArguments):
    apply: ConsumableApplyMapping


class ConsumableSeriesArguments(WhereArguments):
    apply: SeriesWhereMapping


class ConsumableCommandHandler:

    @classmethod
    def new(cls, args: ConsumableNewArguments) -> str:
        # TODO: Can we do a check to see if something similar already exists?
        consumable = ConsumableHandler.new(**args["new"])
        consumables_list = ConsumableList([consumable], args["date_format"])
        return str(consumables_list)

    @classmethod
    def list(cls, args: WhereArguments) -> str:
        consumables = ConsumableHandler.find(**args["where"])
        consumables_list = ConsumableList(consumables, args["date_format"])
        return str(consumables_list)

    @classmethod
    def update(cls, args: ConsumableUpdateArguments) -> str:
        # TODO: What if no values to set are provided?
        # TODO: Confirm update for multiple hits
        # TODO: What happens if none are found
        # TODO: Tagging
        consumables = ConsumableHandler.update(args["where"], args["apply"])
        consumables_list = ConsumableList(consumables, args["date_format"])
        return str(consumables_list)

    @classmethod
    def delete(cls, args: WhereArguments) -> str:
        # TODO: Confirm delete for multiple hits
        # TODO: How do we know how many are deleted?
        ConsumableHandler.delete(**args["where"])
        return "Done"

    @classmethod
    def series(cls, args: ConsumableSeriesArguments) -> str:
        # TODO: Confirm series for multiple hits
        series = SeriesHandler.find(**args["apply"])
        series_id = series[0].id
        consumables = ConsumableHandler.update(
            args["where"], {"series_id": ApplyQuery(series_id)}
        )
        consumables_list = ConsumableList(consumables, args["date_format"])
        return str(consumables_list)

    @classmethod
    def personnel(cls, args: CommandArgumentsBase) -> str:
        # TODO: Set/remove personnel impl. in backend
        # TODO: Can we just create personnel if they don't exist?
        return str(args)
