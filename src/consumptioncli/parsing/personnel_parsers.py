from argparse import ArgumentParser
from typing import override

from consumptioncli.commands import PersonnelCommandHandler
from consumptioncli.display.lists import PersonnelList, PersonnelOrderKey

from .actions import SubStore
from .BetterNamespace import BetterNamespace
from .parsing import ParserBase
from .types import QueryType, closest_choice_index


class PersonnelParser(ParserBase):
    @override
    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        sub = parser.add_subparsers(title="mode", dest="mode", required=True)

        PersonnelNewParser.setup(sub.add_parser("new", aliases=["n"]))
        PersonnelListParser.setup(sub.add_parser("list", aliases=["l"]))
        PersonnelUpdateParser.setup(sub.add_parser("update", aliases=["u"]))
        PersonnelDeleteParser.setup(sub.add_parser("delete", aliases=["d"]))
        PersonnelViewParser.setup(sub.add_parser("view", aliases=["v"]))

    @classmethod
    def list_fields(cls, parser: ArgumentParser) -> None:
        group = parser.add_argument_group("listing")
        _ = group.add_argument(
            "-o",
            "--order",
            dest="order_key",
            default=PersonnelOrderKey.RATING,
            type=closest_choice_index(
                lambda i: PersonnelList.order_keys()[i], PersonnelList.order_keys()
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


class PersonnelNewParser(ParserBase):
    @override
    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(handler=PersonnelCommandHandler.new, new=BetterNamespace())
        cls.personnel_fields(parser, "new", QueryType.NEW)


class PersonnelListParser(ParserBase):
    @override
    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(
            handler=PersonnelCommandHandler.list, where=BetterNamespace()
        )
        cls.personnel_fields(parser, "where.personnel", QueryType.WHERE, False, True)
        cls.series_fields(parser, "where.series", QueryType.WHERE, True, True)
        cls.consumable_fields(parser, "where.consumable", QueryType.WHERE, True, True)
        PersonnelParser.list_fields(parser)


class PersonnelUpdateParser(ParserBase):
    @override
    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(
            handler=PersonnelCommandHandler.update, where=BetterNamespace()
        )
        cls.personnel_fields(parser, "where.personnel", QueryType.WHERE, False, True)
        cls.series_fields(parser, "where.series", QueryType.WHERE, True, True)
        cls.consumable_fields(parser, "where.consumable", QueryType.WHERE, True, True)

        parser_apply = parser.add_subparsers(
            title="apply", dest="subapply", required=True
        ).add_parser(
            "apply",
            aliases=["a"],
        )
        parser_apply.set_defaults(apply=BetterNamespace())
        cls.personnel_fields(parser_apply, "apply", QueryType.APPLY)
        PersonnelParser.list_fields(parser)


class PersonnelDeleteParser(ParserBase):
    @override
    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(
            handler=PersonnelCommandHandler.delete, where=BetterNamespace()
        )
        cls.personnel_fields(parser, "where.personnel", QueryType.WHERE, False, True)
        cls.series_fields(parser, "where.series", QueryType.WHERE, True, True)
        cls.consumable_fields(parser, "where.consumable", QueryType.WHERE, True, True)


class PersonnelViewParser(ParserBase):
    @override
    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(
            handler=PersonnelCommandHandler.view, where=BetterNamespace()
        )
        cls.personnel_fields(parser, "where.personnel", QueryType.WHERE, False, True)
        cls.series_fields(parser, "where.series", QueryType.WHERE, True, True)
        cls.consumable_fields(parser, "where.consumable", QueryType.WHERE, True, True)
