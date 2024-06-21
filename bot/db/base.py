from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Return the table name for a given class.

        This function returns the table name for a given class by converting the
        class name to lowercase and appending 's'.

        Args:
            cls (class): The class for which the table name is to be determined.

        Returns:
            str: The table name for the input class.
        """

        return f"{cls.__name__.lower()}s"

    id = Column(Integer, primary_key=True, autoincrement=True)
