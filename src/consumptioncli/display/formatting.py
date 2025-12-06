from typing import Callable


def truncate(string: str, amount: int = 20) -> str:
    if len(string) > amount:
        diff = min(3, len(string) - amount)
        return string[0 : amount - diff] + "." * diff
    else:
        return string


def s(count: int) -> str:
    return "s" if count != 1 else ""


def q[T](value: T | None, f: Callable[[T], str] = str) -> str:
    return "?" if value is None else f(value)
