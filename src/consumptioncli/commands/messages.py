from collections.abc import Mapping
from typing import Callable

from consumptionbackend.entities import Consumable, EntityBase, Personnel, Series

from consumptioncli.display.formatting import s

names: Mapping[type[EntityBase], Callable[[int], str]] = {
    Consumable: lambda count: Consumable.__name__ + s(count),
    Series: lambda count: Series.__name__,
    Personnel: lambda count: Personnel.__name__,
}


NO_UPDATES = "No updates specified."


def entity_to_str(entity: EntityBase) -> str:
    match entity:
        case Consumable():
            return f"#{entity.id} [{entity.type}] {entity.name}"
        case Series():
            return f"#{entity.id} {entity.name}"
        case Personnel():
            return f"#{entity.id} {entity.full_name()}"
        case _:
            return f"#{entity.id}"


def matching(t: type[EntityBase], count: int) -> str:
    return f"{count} matched {names[t](count)}."


def no_matching(t: type[EntityBase]) -> str:
    return f"No matching {names[t](1)}."


def similar(t: type[EntityBase], count: int) -> str:
    return f"{count} similar {names[t](count)} found."


def cancelled_new(t: type[EntityBase]) -> str:
    return f"{names[t](1)} creation cancelled."


def update_many(t: type[EntityBase], count: int) -> str:
    return f"update of {count} {names[t](count)}"


def cancelled_update(t: type[EntityBase]) -> str:
    return f"{names[t](1)} update cancelled."


def cancelled_relation_update(t1: type[EntityBase], t2: type[EntityBase]) -> str:
    return f"{names[t1](1)} {names[t2](1)} update cancelled."


def delete_many(t: type[EntityBase], count: int) -> str:
    return f"deletion of {count} {names[t](count)}"


def cancelled_deletion(t: type[EntityBase]) -> str:
    return f"{names[t](1)} deletion cancelled."


def deleted(t: type[EntityBase], count: int) -> str:
    return f"{count} {names[t](count)} deleted."


def selection(entity: EntityBase) -> str:
    return f"selection of {entity_to_str(entity)}"


def none_selected(t: type[EntityBase]) -> str:
    return f"No {names[t](1)} selected."


def change(t1: type[EntityBase], t2: type[EntityBase], count: int) -> str:
    return f"change of {names[t1](1)} for {count} {names[t2](count)}"
