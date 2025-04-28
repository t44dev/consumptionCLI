# stdlib
from argparse import Action, ArgumentParser, Namespace
from collections.abc import MutableMapping, Sequence
from typing import Any

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
        current: MutableMapping[str, Any] | Namespace = namespace

        for name in dests:
            if name not in current:
                if isinstance(current, Namespace):
                    setattr(current, name, dict())
                else:
                    current[name] = dict()
            if isinstance(current, Namespace):
                current = getattr(current, name)
            else:
                current = current[name]

        if isinstance(current, Namespace):
            setattr(current, dest, values)
        else:
            current[dest] = values
