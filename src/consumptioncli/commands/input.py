from collections.abc import Sequence

from consumptionbackend.entities import EntityBase

from consumptioncli.commands.messages import (
    matching,
    selection,
    similar,
)


def confirm_action(action: str) -> bool:
    prompt = f"Confirm {action} [Y/n]: "
    response = input(prompt).strip().lower()

    while response not in ["y", "n"]:
        print("Invalid input.")
        response = input(prompt).strip().lower()

    return response == "y"


def confirm_existing(t: type[EntityBase], existing: int) -> bool:
    if existing > 0:
        print(similar(t, existing))
        if not confirm_action("creation"):
            return False
    return True


def confirm_many(count: int, prompt: str) -> bool:
    if count > 1:
        return confirm_action(prompt)
    return True


def select_one[T: EntityBase](entities: Sequence[T]) -> T | None:
    if len(entities) == 1:
        return entities[0]

    selected = None
    t = type(entities[0])

    print(matching(t, len(entities)))
    for entity in entities:
        if confirm_action(selection(entity)):
            selected = entity
            break

    return selected
