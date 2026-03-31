from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.role import Role, user_role_association # noqa


class User(Base):
    """Пользователь"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    first_name: Mapped[str] = mapped_column(String(200))
    last_name: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        autoincrement=True,
        unique=True
    )
    password: Mapped[str] = mapped_column(String(200))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    role: Mapped["Role"] = relationship(
        "Role",
        secondary="user_role_association",
        back_populates="users",
        lazy="selectin"
    )
