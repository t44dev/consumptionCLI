from enum import StrEnum
from typing import Any

from consumptionbackend.database import (
    SeriesApplyMapping,
    SeriesFieldsRequired,
    SeriesService,
    WhereMapping,
    series_required_to_where,
)
from consumptionbackend.entities import Series
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
    cancelled_update,
    delete_many,
    deleted,
    no_matching,
    none_selected,
    update_many,
)
from consumptioncli.display.lists import SeriesList
from consumptioncli.display.types import SeriesContainer
from consumptioncli.display.views import SeriesView


class SeriesCommandHandler:
    @classmethod
    def new(
        cls, *, force: bool, date_format: str, new: SeriesFieldsRequired, **_: Any
    ) -> str:
        series_service = ServiceProvider.get(SeriesService)

        if not force:
            existing = len(series_service.find(**series_required_to_where(new)))

            if not confirm_existing(Series, existing):
                return cancelled_new(Series)

        series_id = series_service.new(**new)
        series = series_container(
            series_service.find_by_id(series_id), include_consumables=False
        )

        series_view = SeriesView(series, date_format)
        return str(series_view)

    @classmethod
    def list(
        cls,
        *,
        order_key: StrEnum,
        reverse: bool,
        date_format: str,
        where: WhereMapping,
        **_: Any,
    ) -> str:
        series_service = ServiceProvider.get(SeriesService)

        series = [series_container(s) for s in series_service.find(**where)]

        series_list = SeriesList(
            series, order_key=order_key, reverse=reverse, date_format=date_format
        )
        return str(series_list)

    @classmethod
    def update(
        cls,
        *,
        force: bool,
        order_key: StrEnum,
        reverse: bool,
        date_format: str,
        where: WhereMapping,
        apply: SeriesApplyMapping,
        **_: Any,
    ) -> str:
        if len(apply) == 0:
            return NO_UPDATES

        series_service = ServiceProvider.get(SeriesService)

        if not force:
            series = len(series_service.find(**where))
            if not confirm_many(series, update_many(Series, series)):
                return cancelled_update(Series)

        series_ids = series_service.update(where, apply)

        series = [series_container(s) for s in series_service.find_by_ids(series_ids)]

        series_list = SeriesList(
            series, order_key=order_key, reverse=reverse, date_format=date_format
        )
        return str(series_list)

    @classmethod
    def delete(cls, *, force: bool, where: WhereMapping, **_: Any) -> str:
        series_service = ServiceProvider.get(SeriesService)

        if not force:
            series = len(series_service.find(**where))
            if not confirm_many(series, delete_many(Series, series)):
                return cancelled_deletion(Series)

        series_deleted = series_service.delete(**where)
        return deleted(Series, series_deleted)

    @classmethod
    def view(
        cls,
        *,
        force: bool,
        date_format: str,
        where: WhereMapping,
        **_: Any,
    ) -> str:
        series_service = ServiceProvider.get(SeriesService)

        series = series_service.find(**where)
        if len(series) == 0:
            return no_matching(Series)

        selected_series = select_one(series) if not force else series[0]

        if selected_series is None:
            return none_selected(Series)

        series = series_container(selected_series)

        series_view = SeriesView(series, date_format=date_format)
        return str(series_view)


def series_container(
    series: Series, *, include_consumables: bool = True
) -> SeriesContainer:
    series_service = ServiceProvider.get(SeriesService)

    return SeriesContainer(
        series, series_service.consumables(series.id) if include_consumables else None
    )
