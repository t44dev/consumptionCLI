from collections.abc import Sequence
from datetime import datetime

from consumptionbackend.entities import Consumable


def average_rating(consumables: Sequence[Consumable]) -> float | None:
    ratings = [c.rating for c in consumables if c.rating is not None]
    return sum(ratings) / len(ratings) if len(ratings) > 0 else None


def global_start_date(consumables: Sequence[Consumable]) -> datetime | None:
    if len(consumables) == 0:
        return None

    return (
        min([c.start_date for c in consumables if c.start_date is not None])
        if any([c.start_date is not None for c in consumables])
        else None
    )


def global_end_date(consumables: Sequence[Consumable]) -> datetime | None:
    if len(consumables) == 0:
        return None

    return (
        min([c.start_date for c in consumables if c.start_date is not None])
        if all([c.start_date is not None for c in consumables])
        else None
    )


def total_parts(consumables: Sequence[Consumable]) -> int:
    return sum([c.parts for c in consumables])


def total_max_parts(consumables: Sequence[Consumable]) -> int | None:
    return (
        sum([c.max_parts for c in consumables if c.max_parts is not None])
        if any([c.max_parts is not None for c in consumables])
        else None
    )
