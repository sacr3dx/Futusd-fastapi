from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String
from uuid import UUID
import uuid

class Base(DeclarativeBase):
    pass

class UsersModel(Base):
    __tablename__ = "users"

    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    username: Mapped[str] = mapped_column(String(25))
    hashed_password: Mapped[str] = mapped_column(String)