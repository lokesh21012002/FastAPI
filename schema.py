from pydantic import BaseModel, model_validator, field_validator, validator
from typing import Optional, List
from datetime import date
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
    dob: date

    role: List[Role]

    # course = List[]

    class Config:
        orm_mode = True

    # @validator('dob')
    # def check_dob(cls, value):
    #     if value < 0:

    #         raise ValueError("dob cannot be negative")
    #     return value


class UpdateUser(BaseModel):

    name: Optional[str] = None

    # gender: Optional[Gender]
    dob: Optional[date] = 1
    role: Optional[List[Role]] = []

    class Config:
        orm_mode = True


class ResponseEntity:
    id: int
    name: str
    age: int
    role: List[Role]

    def __init__(self, id, name, dob, role):
        self.id = id
        self.name = name
        self.age = dob
        self.role = role

    class Config:
        orm_mode = True
