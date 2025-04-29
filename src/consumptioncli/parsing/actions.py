# stdlib
from argparse import Action, ArgumentParser, Namespace
from collections.abc import Sequence
from typing import Any

# consumption
from .BetterNamespace import BetterNamespace

_T = Any

# Thanks to hpaulj for the main ideas around this implementation https://stackoverflow.com/a/18677482


class SubStore(Action):

    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        values: str | Sequence[Any] | None,
        option_string: str | None = None,
    ) -> None:
        dests = self.dest.split(".")
        dest = dests.pop()
        current: Namespace = namespace

        for name in dests:
            if name not in current:
                setattr(current, name, BetterNamespace())
            current = getattr(current, name)
        setattr(current, dest, values)
