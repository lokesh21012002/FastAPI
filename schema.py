from pydantic import BaseModel, model_validator, field_validator, validator
from typing import Optional, List
from uuid import UUID, uuid4
from enum import Enum

from database import Base


class Gender(str, Enum):
    male = "male"
    female = "female"


class Role(str, Enum):
    user = "user"
    admin = "admin"


class User(BaseModel):
    id: int
    name: str

    # gender: Gender
    age: int

    role: List[Role]

    # course = List[]

    class Config:
        orm_mode = True

    # @validator('age')
    # def check_age(cls, value):
    #     if value < 0:

    #         raise ValueError("Age cannot be negative")
    #     return value


class UpdateUser(BaseModel):

    name: Optional[str] = None

    # gender: Optional[Gender]
    age: Optional[int] = 1
    role: Optional[List[Role]] = []

    class Config:
        orm_mode = True
