# consumption
from consumptionbackend.database import (
    SeriesFieldsRequired,
    SeriesApplyMapping,
)
from .command_handling import CommandArgumentsBase, WhereArguments
from .database import SeriesHandler


class SeriesNewArguments(CommandArgumentsBase):
    new: SeriesFieldsRequired


class SeriesUpdateArguments(WhereArguments):
    apply: SeriesApplyMapping


class SeriesCommandHandler:

    @classmethod
    def new(cls, args: SeriesNewArguments) -> str:
        # TODO: Can we do a check to see if something similar already exists?
        consumable = SeriesHandler.new(**args["new"])
        return str(consumable)

    @classmethod
    def list(cls, args: WhereArguments) -> str:
        consumables = SeriesHandler.find(**args["where"])
        return str(consumables)

    @classmethod
    def update(cls, args: SeriesUpdateArguments) -> str:
        # TODO: What if no values to set are provided?
        # TODO: Confirm update for multiple hits
        # TODO: What happens if none are found
        # TODO: Tagging
        consumables = SeriesHandler.update(args["where"], args["apply"])
        return str(consumables)

    @classmethod
    def delete(cls, args: WhereArguments) -> str:
        # TODO: Confirm delete for multiple hits
        # TODO: How do we know how many are deleted?
        SeriesHandler.delete(**args["where"])
        return "Done"
