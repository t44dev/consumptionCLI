from collections.abc import Sequence
from typing import NamedTuple

from consumptionbackend.entities import EntityBase


class EntityRoles[E: EntityBase](NamedTuple):
    entity: E
    roles: Sequence[str]
