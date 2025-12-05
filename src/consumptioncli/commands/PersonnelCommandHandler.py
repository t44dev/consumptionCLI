# consumption
from enum import StrEnum
from consumptionbackend.database import (
    PersonnelFieldsRequired,
    PersonnelApplyMapping,
)
from consumptioncli.lists import PersonnelList
from .command_handling import CommandArgumentsBase, WhereArguments
from .database import PersonnelHandler


class PersonnelNewCommandArguments(CommandArgumentsBase):
    new: PersonnelFieldsRequired


class PersonnelListCommandArguments(WhereArguments):
    order_key: StrEnum
    reverse: bool


class PersonnelUpdateCommandArguments(WhereArguments):
    apply: PersonnelApplyMapping
    order_key: StrEnum
    reverse: bool


class PersonnelCommandHandler:

    @classmethod
    def new(cls, args: PersonnelNewCommandArguments) -> str:
        # TODO: Can we do a check to see if something similar already exists?
        personnel_id = PersonnelHandler.new(**args["new"])
        personnel = PersonnelHandler.find_by_id(personnel_id)

        personnel_list = PersonnelList([personnel])
        return str(personnel_list)

    @classmethod
    def list(cls, args: PersonnelListCommandArguments) -> str:
        personnel = PersonnelHandler.find(**args["where"])

        personnel_list = PersonnelList(personnel, args["order_key"], args["reverse"])
        return str(personnel_list)

    @classmethod
    def update(cls, args: PersonnelUpdateCommandArguments) -> str:
        # TODO: What if no values to set are provided?
        # TODO: Confirm update for multiple hits
        # TODO: What happens if none are found
        # TODO: Tagging
        personnel_ids = PersonnelHandler.update(args["where"], args["apply"])
        personnel = PersonnelHandler.find_by_ids(personnel_ids)

        personnel_list = PersonnelList(personnel, args["order_key"], args["reverse"])
        return str(personnel_list)

    @classmethod
    def delete(cls, args: WhereArguments) -> str:
        # TODO: Confirm delete for multiple hits
        # TODO: How do we know how many are deleted?
        personnel_deleted = PersonnelHandler.delete(**args["where"])
        return f"{personnel_deleted} Personnel deleted."


# TODO: View command
