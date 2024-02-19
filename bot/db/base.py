from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
