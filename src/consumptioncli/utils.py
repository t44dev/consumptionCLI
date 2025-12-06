from collections.abc import MutableSequence, Sequence
from typing import Callable


def unique[T](f: Callable[[T, T], bool], seq: Sequence[T]) -> Sequence[T]:
    unique: MutableSequence[T] = []

    for item in seq:
        if not any([f(item, other) for other in unique]):
            unique.append(item)

    return unique
