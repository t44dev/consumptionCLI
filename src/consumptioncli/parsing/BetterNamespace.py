# stdlib
from argparse import Namespace
from collections.abc import Iterator, MutableMapping
from typing import Any


class BetterNamespace(Namespace, MutableMapping[str, Any]):

    def __getitem__(self, key: str, /) -> Any:
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any, /) -> None:
        setattr(self, key, value)

    def __delitem__(self, key: str, /) -> None:
        delattr(self, key)

    def __iter__(self) -> Iterator[str]:
        return iter(vars(self))

    def __len__(self) -> int:
        return len(vars(self))
