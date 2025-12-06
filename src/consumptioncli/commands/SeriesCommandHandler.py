from enum import StrEnum
from typing import Any, cast
from consumptionbackend.database import (
    SeriesApplyMapping,
    SeriesFieldsRequired,
    SeriesWhereMapping,
    WhereMapping,
    WhereQuery,
)

from consumptioncli.lists import SeriesList
from consumptioncli.utils import confirm_action

from .command_handling import CommandArgumentsBase, WhereArguments
from .database import SeriesHandler


class SeriesNewArguments(CommandArgumentsBase):
    new: SeriesFieldsRequired


class SeriesUpdateArguments(WhereArguments):
    apply: SeriesApplyMapping


class SeriesCommandHandler:
    @classmethod
    def new(cls, *, force: bool, new: SeriesFieldsRequired, **_: Any) -> str:
        if not force:
            where: SeriesWhereMapping = cast(
                SeriesWhereMapping,
                cast(object, {k: [WhereQuery(v)] for k, v in new.items()}),
            )
            existing = len(SeriesHandler.find(series=where))
            if existing > 0:
                print(f"{existing} similar Series found.")
                if not confirm_action("creation"):
                    return "Series creation cancelled."

        series_id = SeriesHandler.new(**new)
        series = SeriesHandler.find_by_id(series_id)

        series_list = SeriesList([series])
        return str(series_list)

    @classmethod
    def list(
        cls, *, order_key: StrEnum, reverse: bool, where: WhereMapping, **_
    ) -> str:
        series = SeriesHandler.find(**where)

        series_list = SeriesList(series, order_key, reverse)
        return str(series_list)

    @classmethod
    def update(
        cls,
        *,
        force: bool,
        order_key: StrEnum,
        reverse: bool,
        where: WhereMapping,
        apply: SeriesApplyMapping,
        **_: Any,
    ) -> str:
        if len(apply) == 0:
            return "No updates specified."

        if not force:
            series = len(SeriesHandler.find(**where))
            if series > 1 and not confirm_action(f"update of {series} Series"):
                return "Series update cancelled."

        # TODO: What happens if none are found
        series_ids = SeriesHandler.update(where, apply)
        series = SeriesHandler.find_by_ids(series_ids)

        series_list = SeriesList(series, order_key, reverse)
        return str(series_list)

    @classmethod
    def delete(cls, *, force: bool, where: WhereMapping, **_: Any) -> str:
        if not force:
            existing = len(SeriesHandler.find(**where))
            if existing > 1:
                print(f"{existing} Series found.")
                if not confirm_action("deletion"):
                    return "Series deletion cancelled."

        series_deleted = SeriesHandler.delete(**where)
        return f"{series_deleted} Series deleted."


# TODO: View command
