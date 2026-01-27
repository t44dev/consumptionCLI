from argparse import Namespace
from collections.abc import Callable, Mapping, Sequence, Set
from dataclasses import dataclass
from datetime import datetime
from difflib import get_close_matches
from enum import IntEnum
from typing import Any, cast

from consumptionbackend.database import (
    ApplyOperator,
    ApplyQuery,
    WhereOperator,
    WhereQuery,
)
from consumptionbackend.entities import Status

from .operators import ApplyOperators, WhereOperators


class QueryType(IntEnum):
    NEW = 0
    WHERE = 1
    APPLY = 2


# Consumable Types


def consumable_status(value: str) -> Status:
    # TODO: Consider using difflab here
    for s in Status:
        # Accept integer specification
        try:
            int_val = int(value)
            if int_val == int(s):
                return s
        except ValueError:
            ...

        # Accept prefix/full name with any casing
        if s.name.lower().startswith(value.lower()):
            return s

    raise ValueError(
        f"Invalid status specified. Status must be one of {[s.name for s in Status]}."
    )


# Wrappers


def sequence[T](fn: Callable[[str], T]) -> Callable[[str], Sequence[T]]:
    def convert_sequence(value: str) -> Sequence[T]:
        values = value.split(",")
        return [fn(e) for e in values]

    return convert_sequence


def noneable[T](fn: Callable[[str], T]) -> Callable[[str], T | None]:
    return lambda value: (
        fn(value) if value.lower() not in ["?", "null", "none"] else None
    )


def closest_choice_index[T](
    fn: Callable[[int], T], choices: Sequence[str]
) -> Callable[[str], T]:
    choices_lower = [c.lower() for c in choices]

    def convert_closest_choice_index(value: str) -> T:
        closest_matches = get_close_matches(value.lower(), choices_lower, n=1, cutoff=0)
        return fn(choices_lower.index(closest_matches[0]))

    return convert_closest_choice_index


def query_selector[T](
    type: Callable[[str], T],
    query_type: QueryType,
    where_operators: WhereOperators,
    apply_operators: ApplyOperators,
) -> Callable[[str], T | Sequence[WhereQuery[T]] | ApplyQuery[T]]:
    return (
        type
        if query_type is QueryType.NEW
        else (
            sequence(where_query(type, **where_operators))
            if query_type is QueryType.WHERE
            else apply_query(type, **apply_operators)
        )
    )


where_operator_map: Mapping[WhereOperator, str] = {
    WhereOperator.EQ: "=",
    WhereOperator.NEQ: "!",
    WhereOperator.GT: ">",
    WhereOperator.GTE: ">=",
    WhereOperator.LT: "<",
    WhereOperator.LTE: "<=",
    WhereOperator.LIKE: "~",
}


def where_query[T](
    fn: Callable[[str], T],
    allowed_operators: Set[WhereOperator],
    default_operator: WhereOperator,
) -> Callable[[str], WhereQuery[T]]:
    if len(allowed_operators) == 0:
        raise RuntimeError("At least one allowed operator must be specified.")

    def converter(value: str) -> WhereQuery[T]:
        if len(value) == 0:
            raise ValueError("Value too short.")

        chosen_operator: None | WhereOperator = None
        for operator in allowed_operators:
            if value.startswith(where_operator_map[operator]) and (
                chosen_operator is None
                or len(where_operator_map[chosen_operator])
                < len(where_operator_map[operator])
            ):
                chosen_operator = operator

        if chosen_operator is None:
            chosen_operator = default_operator
        else:
            value = value[len(where_operator_map[chosen_operator]) :]

        return WhereQuery(fn(value), chosen_operator)

    return converter


apply_operator_map: Mapping[ApplyOperator, str] = {
    ApplyOperator.APPLY: "=",
    ApplyOperator.ADD: "^",
    ApplyOperator.SUB: ".",
}


def apply_query[T](
    fn: Callable[[str], T],
    allowed_operators: Set[ApplyOperator],
    default_operator: ApplyOperator,
) -> Callable[[str], ApplyQuery[T]]:
    if len(allowed_operators) == 0:
        raise RuntimeError("At least one allowed operator must be specified.")

    def converter(value: str) -> ApplyQuery[T]:
        if len(value) == 0:
            raise ValueError("Value too short.")

        chosen_operator: None | ApplyOperator = None
        for operator in allowed_operators:
            if value.startswith(apply_operator_map[operator]) and (
                chosen_operator is None
                or len(apply_operator_map[chosen_operator])
                < len(apply_operator_map[operator])
            ):
                chosen_operator = operator

        if chosen_operator is None:
            chosen_operator = default_operator
        else:
            value = value[len(apply_operator_map[chosen_operator]) :]

        return ApplyQuery(fn(value), chosen_operator)

    return converter


# Post Processing


@dataclass
class DateTimePlaceholder:
    value: str


def datetime_placeholder(value: str) -> DateTimePlaceholder:
    return DateTimePlaceholder(value)


def post_process(value: object, date_format: str) -> Any:
    if isinstance(value, Namespace):
        v = vars(value)
        for key in vars(value):
            setattr(value, key, post_process(v[key], date_format))

    elif isinstance(value, WhereQuery) or isinstance(value, ApplyQuery):
        container = cast(WhereQuery[Any] | ApplyQuery[Any], value)
        container.value = post_process(container.value, date_format)
        return container

    elif isinstance(value, DateTimePlaceholder):
        return datetime.strptime(value.value, date_format)

    elif isinstance(value, list):
        container = cast(list[Any], value)
        return [post_process(e, date_format) for e in container]

    return value
