# consumption
from consumptionbackend.database import (
    PersonnelFieldsRequired,
    PersonnelWhereMapping,
    PersonnelApplyMapping,
)
from .command_handling import CommandArgumentsBase
from .database import PersonnelHandler


class PersonnelNewArguments(CommandArgumentsBase):
    new: PersonnelFieldsRequired


class PersonnelWhereArguments(CommandArgumentsBase):
    where: PersonnelWhereMapping


class PersonnelUpdateArguments(PersonnelWhereArguments):
    apply: PersonnelApplyMapping


class PersonnelCommandHandler:

    @classmethod
    def new(cls, args: PersonnelNewArguments) -> str:
        # TODO: Can we do a check to see if something similar already exists?
        consumable = PersonnelHandler.new(**args["new"])
        return str(consumable)

    @classmethod
    def list(cls, args: PersonnelWhereArguments) -> str:
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
    def delete(cls, args: PersonnelWhereArguments) -> str:
        # TODO: Confirm delete for multiple hits
        # TODO: How do we know how many are deleted?
        PersonnelHandler.delete(**args["where"])
        return "Done"
