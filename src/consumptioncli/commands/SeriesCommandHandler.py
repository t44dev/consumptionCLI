from enum import StrEnum
from typing import Any

from consumptionbackend.database import (
    SeriesApplyMapping,
    SeriesFieldsRequired,
    WhereMapping,
    series_required_to_where,
)
from consumptionbackend.entities import Series

from consumptioncli.commands.input import (
    confirm_existing,
    confirm_many,
    select_one,
)
from consumptioncli.commands.messages import (
    NO_UPDATES,
    cancelled_deletion,
    cancelled_new,
    cancelled_update,
    delete_many,
    deleted,
    no_matching,
    none_selected,
    update_many,
)
from consumptioncli.display.lists import SeriesList
from consumptioncli.display.views import SeriesView

from .database import SeriesHandler


class SeriesCommandHandler:
    @classmethod
    def new(cls, *, force: bool, new: SeriesFieldsRequired, **_: Any) -> str:
        if not force:
            existing = len(SeriesHandler.find(*series_required_to_where(new)))
            if not confirm_existing(Series, existing):
                return cancelled_new(Series)

        series_id = SeriesHandler.new(**new)
        series = SeriesHandler.find_by_id(series_id)

        series_list = SeriesList([series])
        return str(series_list)

    @classmethod
    def list(
        cls, *, order_key: StrEnum, reverse: bool, where: WhereMapping, **_: Any
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
            return NO_UPDATES

        if not force:
            series = len(SeriesHandler.find(**where))
            if not confirm_many(series, update_many(Series, series)):
                return cancelled_update(Series)

        series_ids = SeriesHandler.update(where, apply)
        series = SeriesHandler.find_by_ids(series_ids)

        series_list = SeriesList(series, order_key, reverse)
        return str(series_list)

    @classmethod
    def delete(cls, *, force: bool, where: WhereMapping, **_: Any) -> str:
        if not force:
            series = len(SeriesHandler.find(**where))
            if not confirm_many(series, delete_many(Series, series)):
                return cancelled_deletion(Series)

        series_deleted = SeriesHandler.delete(**where)
        return deleted(Series, series_deleted)

    @classmethod
    def view(
        cls,
        *,
        force: bool,
        where: WhereMapping,
        **_: Any,
    ) -> str:
        series = SeriesHandler.find(**where)
        if len(series) == 0:
            return no_matching(Series)

        if not force:
            selected_series = select_one(series)
        else:
            selected_series = series[0]

        if selected_series is None:
            return none_selected(Series)

        consumables = SeriesHandler.consumables(selected_series.id)

        return str(SeriesView(selected_series, consumables))
