from enum import Enum

import strawberry


@strawberry.enum
class Gender(Enum):
    Male = "male"
    Female = "female"
