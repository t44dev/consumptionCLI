from argparse import ArgumentParser
from typing import override

from consumptioncli.constants import DEFAULT_DATE_FORMAT

from .actions import SubStore
from .consumable_parsers import ConsumableParser
from .parsing import ParserBase
from .personnel_parsers import PersonnelParser
from .series_parsers import SeriesParser
from .tag_parsers import TagParser


class MainParser(ParserBase):
    @override
    @classmethod
    def get(cls) -> ArgumentParser:
        parser = ArgumentParser(
            description="A CLI tool for tracking media consumption",
        )
        cls.setup(parser)
        return parser

    @override
    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        _ = parser.add_argument(
            "-f",
            "--force",
            dest="force",
            default=False,
            action="store_true",
        )
        _ = parser.add_argument(
            "-df",
            "--dateformat",
            dest="date_format",
            default=DEFAULT_DATE_FORMAT,
            metavar="FORMAT",
            help=f"date format string, e.g {DEFAULT_DATE_FORMAT.replace('%', '%%')}",
            action=SubStore,
        )

        sub = parser.add_subparsers(title="entity", dest="entity", required=True)

        ConsumableParser.setup(sub.add_parser("consumable", aliases=["c"]))
        SeriesParser.setup(sub.add_parser("series", aliases=["s"]))
        PersonnelParser.setup(sub.add_parser("personnel", aliases=["p"]))
        TagParser.setup(sub.add_parser("tag", aliases=["t"]))
