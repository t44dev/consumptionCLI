from argparse import ArgumentParser
from typing import override

from consumptioncli.commands import ConsumableCommandHandler
from consumptioncli.display.lists import ConsumableList, ConsumableOrderKey

from .actions import SubStore
from .BetterNamespace import BetterNamespace
from .operators import role_tag_apply
from .parsing import ParserBase
from .types import QueryType, apply_query, closest_choice_index, sequence


class ConsumableParser(ParserBase):
    @override
    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        sub = parser.add_subparsers(title="mode", dest="mode", required=True)

        ConsumableNewParser.setup(sub.add_parser("new", aliases=["n"]))
        ConsumableListParser.setup(sub.add_parser("list", aliases=["l"]))
        ConsumableUpdateParser.setup(sub.add_parser("update", aliases=["u"]))
        ConsumableDeleteParser.setup(sub.add_parser("delete", aliases=["d"]))
        ConsumableApplySeriesParser.setup(sub.add_parser("series", aliases=["s"]))
        ConsumableChangePersonnelParser.setup(
            sub.add_parser("personnel", aliases=["p"])
        )
        ConsumableViewParser.setup(sub.add_parser("view", aliases=["v"]))

    @classmethod
    def list_fields(cls, parser: ArgumentParser) -> None:
        group = parser.add_argument_group("listing")
        _ = group.add_argument(
            "-o",
            "--order",
            dest="order_key",
            default=ConsumableOrderKey.RATING,
            type=closest_choice_index(
                lambda i: ConsumableList.order_keys()[i], ConsumableList.order_keys()
            ),
            metavar="ORDER",
            action=SubStore,
        )
        _ = group.add_argument(
            "--reverse",
            dest="reverse",
            const=True,
            default=False,
            nargs=0,
            action=SubStore,
        )


class ConsumableNewParser(ParserBase):
    @override
    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(handler=ConsumableCommandHandler.new, new=BetterNamespace())
        cls.consumable_fields(parser, "new", QueryType.NEW)


class ConsumableListParser(ParserBase):
    @override
    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(
            handler=ConsumableCommandHandler.list, where=BetterNamespace()
        )
        cls.consumable_fields(parser, "where.consumable", QueryType.WHERE, False, True)
        cls.series_fields(parser, "where.series", QueryType.WHERE, True, True)
        cls.personnel_fields(parser, "where.personnel", QueryType.WHERE, True, True)
        ConsumableParser.list_fields(parser)


class ConsumableUpdateParser(ParserBase):
    @override
    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(
            handler=ConsumableCommandHandler.update,
            where=BetterNamespace(),
        )
        cls.consumable_fields(parser, "where.consumable", QueryType.WHERE, False, True)
        cls.series_fields(parser, "where.series", QueryType.WHERE, True, True)
        cls.personnel_fields(parser, "where.personnel", QueryType.WHERE, True, True)

        parser_apply = parser.add_subparsers(
            title="apply", dest="subapply", required=True
        ).add_parser(
            "apply",
            aliases=["a"],
        )
        parser_apply.set_defaults(apply=BetterNamespace())
        cls.consumable_fields(parser_apply, "apply", QueryType.APPLY)
        ConsumableParser.list_fields(parser)


class ConsumableDeleteParser(ParserBase):
    @override
    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(
            handler=ConsumableCommandHandler.delete, where=BetterNamespace()
        )
        cls.consumable_fields(parser, "where.consumable", QueryType.WHERE, False, True)
        cls.series_fields(parser, "where.series", QueryType.WHERE, True, True)
        cls.personnel_fields(parser, "where.personnel", QueryType.WHERE, True, True)


class ConsumableApplySeriesParser(ParserBase):
    @override
    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(
            handler=ConsumableCommandHandler.series,
            where=BetterNamespace(),
        )
        cls.consumable_fields(parser, "where.consumable", QueryType.WHERE, False, True)
        cls.series_fields(parser, "where.series", QueryType.WHERE, True, True)
        cls.personnel_fields(parser, "where.personnel", QueryType.WHERE, True, True)

        parser_apply = parser.add_subparsers(
            title="apply", dest="subapply", required=True
        ).add_parser(
            "apply",
            aliases=["a"],
        )
        parser_apply.set_defaults(apply=BetterNamespace())
        cls.series_fields(parser_apply, "apply.series", QueryType.WHERE, False, True)
        cls.consumable_fields(
            parser_apply, "apply.consumable", QueryType.WHERE, True, True
        )
        cls.personnel_fields(
            parser_apply, "apply.personnel", QueryType.WHERE, True, True
        )
        ConsumableParser.list_fields(parser)


class ConsumableChangePersonnelParser(ParserBase):
    @override
    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(
            handler=ConsumableCommandHandler.personnel,
            consumable_where=BetterNamespace(),
            personnel_where=BetterNamespace(),
        )
        cls.consumable_fields(
            parser, "consumable_where.consumable", QueryType.WHERE, False, True
        )
        cls.series_fields(
            parser, "consumable_where.series", QueryType.WHERE, True, True
        )
        cls.personnel_fields(
            parser, "consumable_where.personnel", QueryType.WHERE, True, True
        )

        parser_apply = parser.add_subparsers(
            title="apply", dest="subapply", required=True
        ).add_parser(
            "apply",
            aliases=["a"],
        )
        parser_apply.set_defaults(apply=BetterNamespace())
        cls.consumable_fields(
            parser_apply, "personnel_where.consumable", QueryType.WHERE, True, True
        )
        cls.series_fields(
            parser_apply, "personnel_where.series", QueryType.WHERE, True, True
        )
        cls.personnel_fields(
            parser_apply, "personnel_where.personnel", QueryType.WHERE, False, True
        )

        _ = parser_apply.add_argument(
            "-r",
            "--role",
            dest="roles",
            type=sequence(apply_query(str, **role_tag_apply)),
            action=SubStore,
            required=True,
        )


class ConsumableViewParser(ParserBase):
    @override
    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(
            handler=ConsumableCommandHandler.view, where=BetterNamespace()
        )
        cls.consumable_fields(parser, "where.consumable", QueryType.WHERE, False, True)
        cls.series_fields(parser, "where.series", QueryType.WHERE, True, True)
        cls.personnel_fields(parser, "where.personnel", QueryType.WHERE, True, True)
