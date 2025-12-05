from consumptionbackend.database import (
    SeriesApplyMapping,
    SeriesFieldsRequired,
)

from consumptioncli.lists import SeriesList

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
        series_id = SeriesHandler.new(**args["new"])
        series = SeriesHandler.find_by_id(series_id)

        series_list = SeriesList([series])
        return str(series_list)

    @classmethod
    def list(cls, args: WhereArguments) -> str:
        series = SeriesHandler.find(**args["where"])

        series_list = SeriesList(series)
        return str(series_list)

    @classmethod
    def update(cls, args: SeriesUpdateArguments) -> str:
        # TODO: What if no values to set are provided?
        # TODO: Confirm update for multiple hits
        # TODO: What happens if none are found
        # TODO: Tagging
        series_ids = SeriesHandler.update(args["where"], args["apply"])
        series = SeriesHandler.find_by_ids(series_ids)

        series_list = SeriesList(series)
        return str(series_list)

    @classmethod
    def delete(cls, args: WhereArguments) -> str:
        # TODO: Confirm delete for multiple hits
        # TODO: How do we know how many are deleted?
        series_deleted = SeriesHandler.delete(**args["where"])
        return f"{series_deleted} Series deleted."


# TODO: View command
