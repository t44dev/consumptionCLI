# consumption
from consumptionbackend.database import (
    PersonnelFieldsRequired,
    PersonnelApplyMapping,
)
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
        consumable = PersonnelHandler.new(**args["new"])
        return str(consumable)

    @classmethod
    def list(cls, args: WhereArguments) -> str:
        consumables = PersonnelHandler.find(**args["where"])
        return str(consumables)

    @classmethod
    def update(cls, args: PersonnelUpdateArguments) -> str:
        # TODO: What if no values to set are provided?
        # TODO: Confirm update for multiple hits
        # TODO: What happens if none are found
        # TODO: Tagging
        consumables = PersonnelHandler.update(args["where"], args["apply"])
        return str(consumables)

    @classmethod
    def delete(cls, args: WhereArguments) -> str:
        # TODO: Confirm delete for multiple hits
        # TODO: How do we know how many are deleted?
        PersonnelHandler.delete(**args["where"])
        return "Done"
