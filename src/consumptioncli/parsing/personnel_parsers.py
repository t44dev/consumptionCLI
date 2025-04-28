# stdlib
from argparse import ArgumentParser

# consumption
from .parsing import ParserBase
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
        parser.set_defaults(handler=PersonnelCommandHandler.new)
        # TODO: Apply args


class PersonnelListParser(ParserBase):
    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(handler=PersonnelCommandHandler.list)
        # TODO: Where args
        # TODO: Order arguments


class PersonnelUpdateParser(ParserBase):

    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(handler=PersonnelCommandHandler.update)
        # TODO: Force update
        # TODO: Where args
        parser_apply = parser.add_subparsers(
            title="apply", dest="subapply", required=True
        ).add_parser(
            "apply",
            aliases=["a"],
        )
        # TODO: Apply args


class PersonnelDeleteParser(ParserBase):

    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        # TODO: Force update
        # TODO: Where args
        parser.set_defaults(handler=PersonnelCommandHandler.delete)
