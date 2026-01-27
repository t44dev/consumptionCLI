from collections.abc import Set
from typing import TypedDict

from consumptionbackend.database import ApplyOperator, WhereOperator


class WhereOperators(TypedDict):
    allowed_operators: Set[WhereOperator]
    default_operator: WhereOperator


class ApplyOperators(TypedDict):
    allowed_operators: Set[ApplyOperator]
    default_operator: ApplyOperator


standard_apply: ApplyOperators = {
    "allowed_operators": {
        ApplyOperator.APPLY,
    },
    "default_operator": ApplyOperator.APPLY,
}

str_where: WhereOperators = {
    "allowed_operators": {
        WhereOperator.EQ,
        WhereOperator.LIKE,
    },
    "default_operator": WhereOperator.LIKE,
}

num_where: WhereOperators = {
    "allowed_operators": {
        WhereOperator.EQ,
        WhereOperator.NEQ,
        WhereOperator.GT,
        WhereOperator.GTE,
        WhereOperator.LT,
        WhereOperator.LTE,
    },
    "default_operator": WhereOperator.EQ,
}

tag_where: WhereOperators = {
    "allowed_operators": {
        WhereOperator.EQ,
        WhereOperator.NEQ,
    },
    "default_operator": WhereOperator.EQ,
}

num_apply: ApplyOperators = {
    "allowed_operators": {
        ApplyOperator.APPLY,
        ApplyOperator.ADD,
        ApplyOperator.SUB,
    },
    "default_operator": ApplyOperator.APPLY,
}

role_tag_apply: ApplyOperators = {
    "allowed_operators": {
        ApplyOperator.APPLY,
        ApplyOperator.ADD,
        ApplyOperator.SUB,
    },
    "default_operator": ApplyOperator.ADD,
}
