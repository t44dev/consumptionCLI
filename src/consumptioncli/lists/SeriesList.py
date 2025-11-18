# stdlib
from collections.abc import Sequence
from enum import StrEnum
from typing import TYPE_CHECKING, Any, final

if TYPE_CHECKING:
    from _typeshed import SupportsRichComparison

# consumable
from consumptionbackend.entities import Series
from consumptioncli.utils import truncate
from .list_handling import EntityList


class SeriesOrderKey(StrEnum):
    NAME = "name"


@final
class SeriesList(EntityList[Series]):

    def __init__(
        self,
        entities: Sequence[Series],
        order_key: StrEnum = SeriesOrderKey.NAME,
        reverse: bool = False,
    ) -> None:
        # TODO: Consumable data i.e. average rating
        super().__init__(
            entities,
            order_key,
            reverse,
        )

    @classmethod
    def order_keys(cls) -> Sequence[StrEnum]:
        return [*super().order_keys(), *list(SeriesOrderKey)]

    @classmethod
    def _headers(cls) -> Sequence[str]:
        return [*super()._headers(), "Name"]

    def _row(self, index: int, element: Series) -> Sequence[Any]:
        # TODO: Average rating column
        # TODO: Total parts column
        return [*super()._row(index, element), truncate(element.name)]

    def _order_key_to_value(
        self, index: int, element: Series, order_key: StrEnum
    ) -> SupportsRichComparison | None:
        match order_key:
            case SeriesOrderKey.NAME:
                return element.name
            case _:
                return super()._order_key_to_value(index, element, order_key)
