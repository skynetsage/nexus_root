from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, TIMESTAMP, ForeignKey, Integer
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from ..engine import base


class UserModel(base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )
    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=True
    )
    email: Mapped[str] = mapped_column(
        String(254), unique=True, index=True, nullable=False
    )
    password: Mapped[str | None] = mapped_column(String(255), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, default=func.now()
    )

    # String-based reference to prevent circular import
    user_resumes: Mapped[list["UserResumeModel"]] = relationship(
        "UserResumeModel", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User {self.id} {self.username} {self.email} {self.is_active}>"
