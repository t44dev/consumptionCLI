# stdlib
from argparse import ArgumentParser


# consumption
from .BetterNamespace import BetterNamespace
from .parsing import ParserBase
from .types import QueryType
from consumptioncli.commands import PersonnelCommandHandler


class PersonnelParser(ParserBase):

    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        sub = parser.add_subparsers(title="mode", dest="mode", required=True)

        PersonnelNewParser.setup(sub.add_parser("new", aliases=["n"]))
        PersonnelListParser.setup(sub.add_parser("list", aliases=["l"]))
        PersonnelUpdateParser.setup(sub.add_parser("update", aliases=["u"]))
        PersonnelDeleteParser.setup(sub.add_parser("delete", aliases=["d"]))


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
        # TODO: Order arguments


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
