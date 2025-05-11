# consumption
from consumptionbackend.database import (
    PersonnelFieldsRequired,
    PersonnelApplyMapping,
)
from consumptioncli.lists import PersonnelList
from .command_handling import CommandArgumentsBase, WhereArguments
from .database import PersonnelHandler


class PersonnelNewArguments(CommandArgumentsBase):
    new: PersonnelFieldsRequired


class PersonnelUpdateArguments(WhereArguments):
    apply: PersonnelApplyMapping


class PersonnelCommandHandler:

    @classmethod
    def new(cls, args: PersonnelNewArguments) -> str:
        # TODO: Can we do a check to see if something similar already exists?
        personnel = PersonnelHandler.new(**args["new"])
        personnel_list = PersonnelList([personnel])
        return str(personnel_list)

    @classmethod
    def list(cls, args: WhereArguments) -> str:
        personnel = PersonnelHandler.find(**args["where"])
        personnel_list = PersonnelList(personnel)
        return str(personnel_list)

    @classmethod
    def update(cls, args: PersonnelUpdateArguments) -> str:
        # TODO: What if no values to set are provided?
        # TODO: Confirm update for multiple hits
        # TODO: What happens if none are found
        # TODO: Tagging
        personnel = PersonnelHandler.update(args["where"], args["apply"])
        personnel_list = PersonnelList(personnel)
        return str(personnel_list)

    @classmethod
    def delete(cls, args: WhereArguments) -> str:
        # TODO: Confirm delete for multiple hits
        # TODO: How do we know how many are deleted?
        PersonnelHandler.delete(**args["where"])
        return "Done"


# TODO: View command
