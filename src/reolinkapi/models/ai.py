"""AI Models"""

from enum import Enum


class AITypes(str, Enum):
    """AI Types"""

    ANIMAL = "animal"
    PET = "dog_cat"
    FACE = "face"
    PEOPLE = "people"
    VEHICLE = "vehicle"
