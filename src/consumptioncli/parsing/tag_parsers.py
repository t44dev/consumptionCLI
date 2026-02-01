from argparse import ArgumentParser
from typing import override

from consumptioncli.commands import TagCommandHandler
from consumptioncli.display.lists import TagList
from consumptioncli.display.lists.TagList import TagOrderKey

from .actions import SubStore
from .BetterNamespace import BetterNamespace
from .parsing import ParserBase
from .types import closest_choice_index


class TagParser(ParserBase):
    @classmethod
    @override
    def setup(cls, parser: ArgumentParser) -> None:
        sub = parser.add_subparsers(title="mode", dest="mode", required=True)

        TagListParser.setup(sub.add_parser("list", aliases=["l"]))

    @classmethod
    def list_fields(cls, parser: ArgumentParser) -> None:
        group = parser.add_argument_group("listing")
        _ = group.add_argument(
            "-o",
            "--order",
            dest="order_key",
            default=TagOrderKey.TAG,
            type=closest_choice_index(
                lambda i: TagList.order_keys()[i], TagList.order_keys()
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


class TagListParser(ParserBase):
    @classmethod
    @override
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(handler=TagCommandHandler.list, where=BetterNamespace())

        TagParser.list_fields(parser)
