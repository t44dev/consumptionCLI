from argparse import Namespace
from collections.abc import Iterator, MutableMapping
from typing import Any, override


class BetterNamespace(Namespace, MutableMapping[str, Any]):
    @override
    def __getitem__(self, key: str, /) -> Any:
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(key)

    @override
    def __setitem__(self, key: str, value: Any, /) -> None:
        setattr(self, key, value)

    @override
    def __delitem__(self, key: str, /) -> None:
        try:
            delattr(self, key)
        except AttributeError:
            raise KeyError(key)

    @override
    def __iter__(self) -> Iterator[str]:
        return iter(vars(self))

    @override
    def __len__(self) -> int:
        return len(vars(self))
