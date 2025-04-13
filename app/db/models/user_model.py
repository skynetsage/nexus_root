from app.db.base import Base
# from app.db.associations import user_role
# from app.db.models.role_model import Role
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, index=True, autoincrement=True
    )
    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=True
    )
    email: Mapped[str] = mapped_column(
        String(254), unique=True, index=True, nullable=True
    )
    password: Mapped[str] = mapped_column(String(255), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def to_dict(self):
        # Include the fields you want to expose
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_verified": self.is_verified,
            "is_active": self.is_active,
        }

    def __repr__(self) -> str:
        return f"<User {self.id} {self.username} {self.email} {self.is_active}>"
