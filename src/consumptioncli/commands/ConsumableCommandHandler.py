# consumption
from consumptionbackend.database import (
    ConsumableFieldsRequired,
    ConsumableApplyMapping,
)
from .command_handling import CommandArgumentsBase, WhereArguments
from .database import ConsumableHandler


class ConsumableNewArguments(CommandArgumentsBase):
    new: ConsumableFieldsRequired


class ConsumableUpdateArguments(WhereArguments):
    apply: ConsumableApplyMapping


class ConsumableCommandHandler:

    @classmethod
    def new(cls, args: ConsumableNewArguments) -> str:
        # TODO: Can we do a check to see if something similar already exists?
        consumable = ConsumableHandler.new(**args["new"])
        return str(consumable)

    @classmethod
    def list(cls, args: WhereArguments) -> str:
        consumables = ConsumableHandler.find(**args["where"])
        return str(consumables)

    @classmethod
    def update(cls, args: ConsumableUpdateArguments) -> str:
        # TODO: What if no values to set are provided?
        # TODO: Confirm update for multiple hits
        # TODO: What happens if none are found
        # TODO: Tagging
        consumables = ConsumableHandler.update(args["where"], args["apply"])
        return str(consumables)

    @classmethod
    def delete(cls, args: WhereArguments) -> str:
        # TODO: Confirm delete for multiple hits
        # TODO: How do we know how many are deleted?
        ConsumableHandler.delete(**args["where"])
        return "Done"

    @classmethod
    def series(cls, args: CommandArgumentsBase) -> str:
        # TODO: Set series impl. in backend
        # TODO: Confirm series for multiple hits
        return str(args)

    @classmethod
    def personnel(cls, args: CommandArgumentsBase) -> str:
        # TODO: Set/remove personnel impl. in backend
        # TODO: Can we just create personnel if they don't exist?
        return str(args)
