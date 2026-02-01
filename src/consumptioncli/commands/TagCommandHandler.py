from enum import StrEnum
from typing import Any

from consumptionbackend.database import ConsumableService, TagService, WhereQuery
from consumptionbackend.utils import ServiceProvider

from consumptioncli.display.lists import TagList
from consumptioncli.display.types import TagContainer


class TagCommandHandler:
    @classmethod
    def list(cls, *, order_key: StrEnum, reverse: bool, **_: Any) -> str:
        tag_service = ServiceProvider.get(TagService)

        tags = [tag_container(t) for t in tag_service.find()]

        tag_list = TagList(tags, order_key=order_key, reverse=reverse)

        return str(tag_list)


def tag_container(tag: str, *, include_consumables: bool = True):
    consumable_service = ServiceProvider.get(ConsumableService)

    return TagContainer(
        tag,
        consumable_service.find(consumables={"tags": [WhereQuery(tag)]})
        if include_consumables
        else None,
    )
