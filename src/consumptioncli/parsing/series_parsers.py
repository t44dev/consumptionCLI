# stdlib
from argparse import ArgumentParser

# consumption
from .BetterNamespace import BetterNamespace
from .parsing import ParserBase, QueryType
from consumptioncli.commands import SeriesCommandHandler


class SeriesParser(ParserBase):

    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        sub = parser.add_subparsers(title="mode", dest="mode", required=True)

        SeriesNewParser.setup(sub.add_parser("new", aliases=["n"]))
        SeriesListParser.setup(sub.add_parser("list", aliases=["l"]))
        SeriesUpdateParser.setup(sub.add_parser("update", aliases=["u"]))
        SeriesDeleteParser.setup(sub.add_parser("delete", aliases=["d"]))


class SeriesNewParser(ParserBase):
    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(handler=SeriesCommandHandler.new, new=BetterNamespace())
        cls.series_fields(parser, "new", QueryType.NEW)


class SeriesListParser(ParserBase):
    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(handler=SeriesCommandHandler.list, where=BetterNamespace())
        cls.series_fields(parser, "where.series", QueryType.WHERE, False, True)
        cls.consumable_fields(parser, "where.consumable", QueryType.WHERE, True, True)
        cls.personnel_fields(parser, "where.personnel", QueryType.WHERE, True, True)
        # TODO: Order arguments


class SeriesUpdateParser(ParserBase):

    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(
            handler=SeriesCommandHandler.update,
            where=BetterNamespace(),
        )
        cls.series_fields(parser, "where.series", QueryType.WHERE, False, True)
        cls.consumable_fields(parser, "where.consumable", QueryType.WHERE, True, True)
        cls.personnel_fields(parser, "where.personnel", QueryType.WHERE, True, True)
        # TODO: Force update

        parser_apply = parser.add_subparsers(
            title="apply", dest="subapply", required=True
        ).add_parser(
            "apply",
            aliases=["a"],
        )
        parser_apply.set_defaults(apply=BetterNamespace())
        cls.series_fields(parser_apply, "apply", QueryType.APPLY)


class SeriesDeleteParser(ParserBase):

    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(
            handler=SeriesCommandHandler.delete, where=BetterNamespace()
        )
        cls.series_fields(parser, "where.series", QueryType.WHERE, False, True)
        cls.consumable_fields(parser, "where.consumable", QueryType.WHERE, True, True)
        cls.personnel_fields(parser, "where.personnel", QueryType.WHERE, True, True)
        # TODO: Force update


# TODO: Add consumables
