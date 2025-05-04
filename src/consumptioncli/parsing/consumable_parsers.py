# stdlib
from argparse import ArgumentParser

# consumption
from .BetterNamespace import BetterNamespace
from .parsing import ParserBase, QueryType
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
        parser.set_defaults(handler=ConsumableCommandHandler.new, new=BetterNamespace())
        cls.consumable_fields(parser, "new", QueryType.NEW)


class ConsumableListParser(ParserBase):

    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(
            handler=ConsumableCommandHandler.list, where=BetterNamespace()
        )
        cls.consumable_fields(parser, "where.consumable", QueryType.WHERE, False, True)
        cls.series_fields(parser, "where.series", QueryType.WHERE, True, True)
        cls.personnel_fields(parser, "where.personnel", QueryType.WHERE, True, True)
        # TODO: Order arguments


class ConsumableUpdateParser(ParserBase):

    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(
            handler=ConsumableCommandHandler.update,
            where=BetterNamespace(),
        )
        cls.consumable_fields(parser, "where.consumable", QueryType.WHERE, False, True)
        cls.series_fields(parser, "where.series", QueryType.WHERE, True, True)
        cls.personnel_fields(parser, "where.personnel", QueryType.WHERE, True, True)
        # TODO: Force update

        parser_apply = parser.add_subparsers(
            title="apply", dest="subapply", required=True
        ).add_parser(
            "apply",
            aliases=["a"],
        )
        parser_apply.set_defaults(apply=BetterNamespace())
        cls.consumable_fields(parser_apply, "apply", QueryType.APPLY)


class ConsumableDeleteParser(ParserBase):

    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(
            handler=ConsumableCommandHandler.delete, where=BetterNamespace()
        )
        cls.consumable_fields(parser, "where.consumable", QueryType.WHERE, False, True)
        cls.series_fields(parser, "where.series", QueryType.WHERE, True, True)
        cls.personnel_fields(parser, "where.personnel", QueryType.WHERE, True, True)
        # TODO: Force update


class ConsumableSetSeriesParser(ParserBase):

    @classmethod
    def setup(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(
            handler=ConsumableCommandHandler.series,
            where=BetterNamespace(),
        )
        cls.consumable_fields(parser, "where.consumable", QueryType.WHERE, False, True)
        cls.series_fields(parser, "where.series", QueryType.WHERE, True, True)
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


# TODO: Add personnel
