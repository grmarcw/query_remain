from sqlalchemy import BIGINT, JSON
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "query_remain"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    recipes: Mapped[dict] = mapped_column(JSON)
    deliveries: Mapped[dict] = mapped_column(JSON, nullable=True)
