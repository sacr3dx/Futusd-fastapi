from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, DATE
from uuid import UUID
import uuid

class Base(DeclarativeBase):
    pass

class CashOutModel(Base):
    __tablename__ = "futusd_db"

    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    base: Mapped[int] = mapped_column(Integer)
    category: Mapped[str] = mapped_column(String(15))
    date: Mapped[str] = mapped_column(DATE)