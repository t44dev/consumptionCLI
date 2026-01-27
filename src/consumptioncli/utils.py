import json
from collections.abc import MutableSequence, Sequence
from pathlib import Path
from typing import Any, Callable, override


def unique[T](f: Callable[[T, T], bool], seq: Sequence[T]) -> Sequence[T]:
    unique: MutableSequence[T] = []

    for item in seq:
        if not any([f(item, other) for other in unique]):
            unique.append(item)

    return unique


class ExtendedEncoder(json.JSONEncoder):
    @override
    def default(self, o: Any) -> Any:
        if isinstance(o, Path):
            return str(o)
        return super().default(o)
