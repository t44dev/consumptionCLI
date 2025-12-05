from typing import TypedDict

from consumptionbackend.database import WhereMapping


class CommandArgumentsBase(TypedDict):
    date_format: str
    force: bool


class WhereArguments(CommandArgumentsBase):
    where: WhereMapping
