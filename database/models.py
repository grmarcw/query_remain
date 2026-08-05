from sqlalchemy import BIGINT, JSON
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class InitialData(Base):
    __tablename__ = "recipes_deliveries"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    recipes: Mapped[dict] = mapped_column(JSON)
    deliveries: Mapped[dict] = mapped_column(JSON, nullable=True)


class SecondaryData(Base):
    __tablename__ = 'daily_usage'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    initial_balance: Mapped[dict] = mapped_column(JSON)
    data: Mapped[dict] = mapped_column(JSON, nullable=True)
