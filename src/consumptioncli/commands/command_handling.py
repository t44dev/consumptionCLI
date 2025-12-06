from typing import TypedDict

from consumptionbackend.database import WhereMapping


class CommandArgumentsBase(TypedDict):
    force: bool
    date_format: str


class WhereArguments(CommandArgumentsBase):
    where: WhereMapping
