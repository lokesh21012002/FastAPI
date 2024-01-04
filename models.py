from pydantic import BaseModel


class Person(BaseModel):
    name: str
    age: int


class Student(Person):

    courses: list
