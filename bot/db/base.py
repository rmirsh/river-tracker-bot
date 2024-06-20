from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id = Column(Integer, primary_key=True, autoincrement=True)
