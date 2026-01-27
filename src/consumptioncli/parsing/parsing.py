from abc import ABC, abstractmethod
from argparse import SUPPRESS, ArgumentParser

from .actions import SubStore
from .operators import (
    num_apply,
    num_where,
    role_tag_apply,
    standard_apply,
    str_where,
    tag_where,
)
from .types import (
    QueryType,
    apply_query,
    consumable_status,
    datetime_placeholder,
    noneable,
    query_selector,
    sequence,
    where_query,
)


class ParserBase(ABC):
    @classmethod
    def get(cls) -> ArgumentParser:
        parser = ArgumentParser()
        cls.setup(parser)
        return parser

    @classmethod
    @abstractmethod
    def setup(cls, parser: ArgumentParser) -> None: ...

    @classmethod
    def consumable_fields(
        cls,
        parser: ArgumentParser,
        dest: str,
        query_type: QueryType,
        prefix_commands: bool = False,
        id: bool = False,
    ):
        prefix = "consumable" if prefix_commands else ""
        short_prefix = prefix[0] if prefix_commands else ""
        group = parser.add_argument_group("consumables")

        if id:
            _ = group.add_argument(
                f"-{short_prefix}i",
                f"--{prefix}id",
                dest=f"{dest}.id",
                type=query_selector(int, query_type, num_where, num_apply),
                action=SubStore,
                default=SUPPRESS,
            )

        _ = group.add_argument(
            f"-{short_prefix}n",
            f"--{prefix}name",
            dest=f"{dest}.name",
            type=query_selector(str, query_type, str_where, standard_apply),
            action=SubStore,
            required=query_type is QueryType.NEW,
            default=SUPPRESS,
        )
        _ = group.add_argument(
            f"-{short_prefix}t",
            f"--{prefix}type",
            dest=f"{dest}.type",
            type=query_selector(str, query_type, str_where, standard_apply),
            action=SubStore,
            required=query_type is QueryType.NEW,
            default=SUPPRESS,
        )
        _ = group.add_argument(
            f"-{short_prefix}s",
            f"--{prefix}status",
            dest=f"{dest}.status",
            type=query_selector(consumable_status, query_type, num_where, num_apply),
            action=SubStore,
            default=SUPPRESS,
        )
        _ = group.add_argument(
            f"-{short_prefix}p",
            f"--{prefix}parts",
            dest=f"{dest}.parts",
            type=query_selector(int, query_type, num_where, num_apply),
            action=SubStore,
            default=SUPPRESS,
        )
        _ = group.add_argument(
            f"-{short_prefix}mp",
            f"--{prefix}maxparts",
            dest=f"{dest}.max_parts",
            type=query_selector(noneable(int), query_type, num_where, num_apply),
            action=SubStore,
            default=SUPPRESS,
        )
        _ = group.add_argument(
            f"-{short_prefix}c",
            f"--{prefix}completions",
            dest=f"{dest}.completions",
            type=query_selector(int, query_type, num_where, num_apply),
            action=SubStore,
            default=SUPPRESS,
        )
        _ = group.add_argument(
            f"-{short_prefix}r",
            f"--{prefix}rating",
            dest=f"{dest}.rating",
            type=query_selector(noneable(float), query_type, num_where, num_apply),
            action=SubStore,
            default=SUPPRESS,
        )
        _ = group.add_argument(
            f"-{short_prefix}sd",
            f"--{prefix}startdate",
            dest=f"{dest}.start_date",
            type=query_selector(
                noneable(datetime_placeholder), query_type, num_where, num_apply
            ),
            action=SubStore,
            default=SUPPRESS,
        )
        _ = group.add_argument(
            f"-{short_prefix}ed",
            f"--{prefix}enddate",
            dest=f"{dest}.end_date",
            type=query_selector(
                noneable(datetime_placeholder), query_type, num_where, num_apply
            ),
            action=SubStore,
            default=SUPPRESS,
        )
        _ = group.add_argument(
            f"--{prefix}tags",
            dest=f"{dest}.tags",
            type=sequence(
                str
                if query_type is QueryType.NEW
                else (
                    where_query(str, **tag_where)
                    if query_type is QueryType.WHERE
                    else apply_query(str, **role_tag_apply)
                )
            ),
            action=SubStore,
            default=SUPPRESS,
        )

    @classmethod
    def series_fields(
        cls,
        parser: ArgumentParser,
        dest: str,
        query_type: QueryType,
        prefix_commands: bool = False,
        id: bool = False,
    ):
        prefix = "series" if prefix_commands else ""
        short_prefix = prefix[0] if prefix_commands else ""
        group = parser.add_argument_group("series")

        if id:
            _ = group.add_argument(
                f"-{short_prefix}i",
                f"--{prefix}id",
                dest=f"{dest}.id",
                type=query_selector(int, query_type, num_where, num_apply),
                action=SubStore,
                default=SUPPRESS,
            )

        _ = group.add_argument(
            f"-{short_prefix}n",
            f"--{prefix}name",
            dest=f"{dest}.name",
            type=query_selector(str, query_type, str_where, standard_apply),
            action=SubStore,
            required=query_type is QueryType.NEW,
            default=SUPPRESS,
        )

    @classmethod
    def personnel_fields(
        cls,
        parser: ArgumentParser,
        dest: str,
        query_type: QueryType,
        prefix_commands: bool = False,
        id: bool = False,
    ):
        prefix = "personnel" if prefix_commands else ""
        short_prefix = prefix[0] if prefix_commands else ""
        group = parser.add_argument_group("personnel")

        if id:
            _ = group.add_argument(
                f"-{short_prefix}i",
                f"--{prefix}id",
                dest=f"{dest}.id",
                type=query_selector(int, query_type, num_where, num_apply),
                action=SubStore,
                default=SUPPRESS,
            )

        _ = group.add_argument(
            f"-{short_prefix}fn",
            f"--{prefix}firstname",
            dest=f"{dest}.first_name",
            type=query_selector(str, query_type, str_where, standard_apply),
            action=SubStore,
            default=SUPPRESS,
        )
        _ = group.add_argument(
            f"-{short_prefix}p",
            f"--{prefix}pseudonym",
            dest=f"{dest}.pseudonym",
            type=query_selector(str, query_type, str_where, standard_apply),
            action=SubStore,
            default=SUPPRESS,
        )
        _ = group.add_argument(
            f"-{short_prefix}ln",
            f"--{prefix}lastname",
            dest=f"{dest}.last_name",
            type=query_selector(str, query_type, str_where, standard_apply),
            action=SubStore,
            default=SUPPRESS,
        )
