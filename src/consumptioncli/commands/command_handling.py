# stdlib
from typing import TypedDict


class CommandArgumentsBase(TypedDict):
    date_format: str
    force: bool
