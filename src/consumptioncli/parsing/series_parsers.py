# stdlib
from argparse import ArgumentParser

# consumption
from .parsing import ParserBase
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
        parser.set_defaults(handler=SeriesCommandHandler.new)
        # TODO: Apply args


class SeriesListParser(ParserBase):
    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(handler=SeriesCommandHandler.list)
        # TODO: Where args
        # TODO: Order arguments


class SeriesUpdateParser(ParserBase):

    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(handler=SeriesCommandHandler.update)
        # TODO: Force update
        # TODO: Where args
        parser_apply = parser.add_subparsers(
            title="apply", dest="subapply", required=True
        ).add_parser(
            "apply",
            aliases=["a"],
        )
        # TODO: Apply args


class SeriesDeleteParser(ParserBase):

    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        # TODO: Force update
        # TODO: Where args
        parser.set_defaults(handler=SeriesCommandHandler.delete)


# TODO: Add consumables
