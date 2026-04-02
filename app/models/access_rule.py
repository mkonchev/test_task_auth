from sqlalchemy import Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.models.role import Role
from app.models.business_element import BusinessElement


class AccessRule(Base):
    __tablename__ = "access_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role_id: Mapped[int] = mapped_column(
        ForeignKey(
            "roles.id",
            ondelete="CASCADE")
        )
    element_id: Mapped[int] = mapped_column(
        ForeignKey(
            "business_elements.id",
            ondelete="CASCADE")
    )

    read_permission: Mapped[bool] = mapped_column(Boolean, default=False)
    read_all_permission: Mapped[bool] = mapped_column(Boolean, default=False)

    create_permission: Mapped[bool] = mapped_column(Boolean, default=False)

    update_permission: Mapped[bool] = mapped_column(Boolean, default=False)
    update_all_permission: Mapped[bool] = mapped_column(Boolean, default=False)

    delete_permission: Mapped[bool] = mapped_column(Boolean, default=False)
    delete_all_permission: Mapped[bool] = mapped_column(Boolean, default=False)

    role: Mapped["Role"] = relationship("Role")
    element: Mapped["BusinessElement"] = relationship("BusinessElement")
