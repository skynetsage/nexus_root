from app.db.base import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..engine import base


class RoleModel(base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    users: Mapped[list["UserModel"]] = relationship(back_populates="role")

    def __repr__(self) -> str:
        return f"<Role {self.id} {self.name} {self.description}>"
