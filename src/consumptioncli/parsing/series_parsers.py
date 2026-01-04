from argparse import ArgumentParser
from typing import override

from consumptioncli.commands import SeriesCommandHandler
from consumptioncli.display.lists import SeriesList, SeriesOrderKey

from .actions import SubStore
from .BetterNamespace import BetterNamespace
from .parsing import ParserBase
from .types import QueryType, closest_choice_index


class SeriesParser(ParserBase):
    @override
    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        sub = parser.add_subparsers(title="mode", dest="mode", required=True)

        SeriesNewParser.setup(sub.add_parser("new", aliases=["n"]))
        SeriesListParser.setup(sub.add_parser("list", aliases=["l"]))
        SeriesUpdateParser.setup(sub.add_parser("update", aliases=["u"]))
        SeriesDeleteParser.setup(sub.add_parser("delete", aliases=["d"]))
        SeriesViewParser.setup(sub.add_parser("view", aliases=["v"]))

    @classmethod
    def list_fields(cls, parser: ArgumentParser) -> None:
        group = parser.add_argument_group("listing")
        _ = group.add_argument(
            "-o",
            "--order",
            dest="order_key",
            default=SeriesOrderKey.RATING,
            type=closest_choice_index(
                lambda i: SeriesList.order_keys()[i], SeriesList.order_keys()
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


class SeriesNewParser(ParserBase):
    @override
    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(handler=SeriesCommandHandler.new, new=BetterNamespace())
        cls.series_fields(parser, "new", QueryType.NEW)


class SeriesListParser(ParserBase):
    @override
    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(handler=SeriesCommandHandler.list, where=BetterNamespace())
        cls.series_fields(parser, "where.series", QueryType.WHERE, False, True)
        cls.consumable_fields(parser, "where.consumable", QueryType.WHERE, True, True)
        cls.personnel_fields(parser, "where.personnel", QueryType.WHERE, True, True)
        SeriesParser.list_fields(parser)


class SeriesUpdateParser(ParserBase):
    @override
    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(
            handler=SeriesCommandHandler.update,
            where=BetterNamespace(),
        )
        cls.series_fields(parser, "where.series", QueryType.WHERE, False, True)
        cls.consumable_fields(parser, "where.consumable", QueryType.WHERE, True, True)
        cls.personnel_fields(parser, "where.personnel", QueryType.WHERE, True, True)

        parser_apply = parser.add_subparsers(
            title="apply", dest="subapply", required=True
        ).add_parser(
            "apply",
            aliases=["a"],
        )
        parser_apply.set_defaults(apply=BetterNamespace())
        cls.series_fields(parser_apply, "apply", QueryType.APPLY)
        SeriesParser.list_fields(parser)


class SeriesDeleteParser(ParserBase):
    @override
    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(
            handler=SeriesCommandHandler.delete, where=BetterNamespace()
        )
        cls.series_fields(parser, "where.series", QueryType.WHERE, False, True)
        cls.consumable_fields(parser, "where.consumable", QueryType.WHERE, True, True)
        cls.personnel_fields(parser, "where.personnel", QueryType.WHERE, True, True)


class SeriesViewParser(ParserBase):
    @override
    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(handler=SeriesCommandHandler.view, where=BetterNamespace())
        cls.series_fields(parser, "where.series", QueryType.WHERE, False, True)
        cls.consumable_fields(parser, "where.consumable", QueryType.WHERE, True, True)
        cls.personnel_fields(parser, "where.personnel", QueryType.WHERE, True, True)
