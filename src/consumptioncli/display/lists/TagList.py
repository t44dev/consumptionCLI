from collections.abc import Sequence
from enum import StrEnum
from typing import Any, final, override

from consumptioncli.display.stats import average_rating
from consumptioncli.display.types import TagContainer

from .list_handling import NOT_APPLICABLE, DisplayListBase


class TagOrderKey(StrEnum):
    TAG = "tag"
    USAGES = "usages"
    RATING = "rating"


@final
class TagList(DisplayListBase[TagContainer]):
    def __init__(
        self,
        tags: Sequence[TagContainer],
        *,
        order_key: StrEnum = TagOrderKey.TAG,
        reverse: bool = False,
    ) -> None:
        super().__init__(tags, order_key=order_key, reverse=reverse)

    @classmethod
    @override
    def order_keys(cls) -> Sequence[StrEnum]:
        return list(TagOrderKey)

    @override
    def _headers(self) -> Sequence[str]:
        headers = ["#", "Tag"]

        if all([t.consumables is not None for t in self.elements]):
            headers.extend(["Usages", "Average Rating"])

        return headers

    @override
    def _row(self, index: int, element: TagContainer) -> Sequence[Any]:
        tag = element.tag
        consumables = element.consumables

        row: Sequence[Any] = [index, tag]

        if consumables is not None:
            row.extend([len(consumables), average_rating(consumables)])

        return row

    @override
    def _footer(self) -> Sequence[Any]:
        footer: Sequence[Any] = [NOT_APPLICABLE, NOT_APPLICABLE]

        if all([t.consumables is not None for t in self.elements]):
            usages = sum(
                [len(t.consumables) for t in self.elements if t.consumables is not None]
            )

            average_ratings = [
                r
                for r in [
                    average_rating(t.consumables)
                    for t in self.elements
                    if t.consumables is not None
                ]
                if r is not None
            ]
            average_average_ratings = (
                (sum(average_ratings) / len(average_ratings))
                if len(average_ratings) > 0
                else None
            )

            footer.extend([usages, average_average_ratings])

        return footer

    @override
    def _order_key_to_value(
        self, index: int, element: TagContainer, order_key: StrEnum
    ) -> Any | None:
        tag = element.tag
        consumables = element.consumables

        match order_key:
            case TagOrderKey.TAG:
                return tag
            case TagOrderKey.USAGES:
                if consumables is not None:
                    return len(consumables)
            case TagOrderKey.RATING:
                if consumables is not None:
                    return average_rating(consumables)
            case _:
                return index
