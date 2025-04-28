# stdlib
from argparse import ArgumentParser

# consumption
from .parsing import ParserBase
from consumptioncli.commands import ConsumableCommandHandler


class ConsumableParser(ParserBase):

    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        sub = parser.add_subparsers(title="mode", dest="mode", required=True)

        ConsumableNewParser.setup(sub.add_parser("new", aliases=["n"]))
        ConsumableListParser.setup(sub.add_parser("list", aliases=["l"]))
        ConsumableUpdateParser.setup(sub.add_parser("update", aliases=["u"]))
        ConsumableDeleteParser.setup(sub.add_parser("delete", aliases=["d"]))


class ConsumableNewParser(ParserBase):

    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(handler=ConsumableCommandHandler.new)
        # TODO: Apply args


class ConsumableListParser(ParserBase):

    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(handler=ConsumableCommandHandler.list)
        # TODO: Where args
        # TODO: Order arguments


class ConsumableUpdateParser(ParserBase):

    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(handler=ConsumableCommandHandler.update)
        # TODO: Force update
        # TODO: Where args
        parser_apply = parser.add_subparsers(
            title="apply", dest="subapply", required=True
        ).add_parser(
            "apply",
            aliases=["a"],
        )
        # TODO: Apply args


class ConsumableDeleteParser(ParserBase):

    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        # TODO: Force update
        # TODO: Where args
        parser.set_defaults(handler=ConsumableCommandHandler.delete)


# TODO: Set series
# TODO: Add personnel
