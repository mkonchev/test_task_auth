from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.user import User # noqa


user_role_association = Table(
    "user_role",
    Base.metadata,
    Column(
        "user_id",
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "role_id",
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True
    )
)


class Role(Base):
    """Роль пользователя"""
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    name: Mapped[str] = mapped_column(String(200))

    users: Mapped[list["User"]] = relationship(
        "User",
        secondary=user_role_association,
        back_populates="role",
        lazy="selectin"
    )
