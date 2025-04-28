# stdlib
from argparse import ArgumentParser

# consumption
from .actions import SubStore
from .parsing import ParserBase
from .consumable_parsers import ConsumableParser
from .series_parsers import SeriesParser
from .personnel_parsers import PersonnelParser


class MainParser(ParserBase):

    @classmethod
    def get(cls) -> ArgumentParser:
        parser = ArgumentParser(
            description="A CLI tool for tracking media consumption",
        )
        cls.setup(parser)
        return parser

    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        _ = parser.add_argument(
            "-df",
            "--dateformat",
            dest="date_format",
            default=r"%Y/%m/%d",
            metavar="FORMAT",
            help="date format string, e.g %%Y/%%m/%%d",
            action=SubStore,
        )

        sub = parser.add_subparsers(title="entity", dest="entity", required=True)

        ConsumableParser.setup(sub.add_parser("consumable", aliases=["c"]))
        SeriesParser.setup(sub.add_parser("series", aliases=["s"]))
        PersonnelParser.setup(sub.add_parser("personnel", aliases=["p"]))
