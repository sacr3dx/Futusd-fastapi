from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, DATE, ForeignKey
from uuid import UUID
import uuid

class Base(DeclarativeBase):
    pass

class CashOutModel(Base):
    __tablename__ = "spending"

    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_uuid: Mapped[UUID] = mapped_column(ForeignKey("users.uuid"), nullable=False)
    base: Mapped[int] = mapped_column(Integer)
    category: Mapped[str] = mapped_column(String(15))
    date: Mapped[str] = mapped_column(DATE)