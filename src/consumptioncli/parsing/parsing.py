# stdlib
from abc import ABC, abstractmethod
from argparse import ArgumentParser


class ParserBase(ABC):

    @classmethod
    def get(cls) -> ArgumentParser:
        parser = ArgumentParser()
        cls.setup(parser)
        return parser

    @classmethod
    @abstractmethod
    def setup(cls, parser: ArgumentParser) -> None:
        pass
