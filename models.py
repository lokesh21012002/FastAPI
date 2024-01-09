from database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType
from uuid import UUID


class Student(Base):
    __tablename__ = 'tmp'

    id = Column(Integer, primary_key=True, index=True,
                autoincrement=True, default=1)
    name = Column(String)
    age = Column(Integer)
    role = Column(MutableList.as_mutable(PickleType),
                  default=[])
