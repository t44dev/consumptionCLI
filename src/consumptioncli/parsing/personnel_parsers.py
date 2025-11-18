# stdlib
from argparse import ArgumentParser


# consumption
from consumptioncli.commands import PersonnelCommandHandler
from consumptioncli.lists import PersonnelList, PersonnelOrderKey
from .BetterNamespace import BetterNamespace
from .parsing import ParserBase
from .actions import SubStore
from .types import QueryType, closest_choice_index


class PersonnelParser(ParserBase):

    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        sub = parser.add_subparsers(title="mode", dest="mode", required=True)

        PersonnelNewParser.setup(sub.add_parser("new", aliases=["n"]))
        PersonnelListParser.setup(sub.add_parser("list", aliases=["l"]))
        PersonnelUpdateParser.setup(sub.add_parser("update", aliases=["u"]))
        PersonnelDeleteParser.setup(sub.add_parser("delete", aliases=["d"]))

    @classmethod
    def list_fields(cls, parser: ArgumentParser) -> None:
        group = parser.add_argument_group("listing")
        _ = group.add_argument(
            "-o",
            "--order",
            dest="order_key",
            default=PersonnelOrderKey.NAME,
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
    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(handler=PersonnelCommandHandler.new, new=BetterNamespace())
        cls.personnel_fields(parser, "new", QueryType.NEW)


class PersonnelListParser(ParserBase):
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

    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(
            handler=PersonnelCommandHandler.update, where=BetterNamespace()
        )
        cls.personnel_fields(parser, "where.personnel", QueryType.WHERE, False, True)
        cls.series_fields(parser, "where.series", QueryType.WHERE, True, True)
        cls.consumable_fields(parser, "where.consumable", QueryType.WHERE, True, True)
        # TODO: Force update

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

    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(
            handler=PersonnelCommandHandler.delete, where=BetterNamespace()
        )
        cls.personnel_fields(parser, "where.personnel", QueryType.WHERE, False, True)
        cls.series_fields(parser, "where.series", QueryType.WHERE, True, True)
        cls.consumable_fields(parser, "where.consumable", QueryType.WHERE, True, True)
        # TODO: Force update
