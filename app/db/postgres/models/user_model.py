from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, TIMESTAMP, ForeignKey, Integer
from sqlalchemy.sql import func
from ..engine import base


class UserModel(base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=True
    )
    email: Mapped[str] = mapped_column(
        String(254), unique=True, index=True, nullable=False
    )
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), nullable=False
    )
    updated_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    role: Mapped["RoleModel"] = relationship(back_populates="users")
    uploads: Mapped[list["FileUploadModel"]] = relationship(back_populates="user")
    resumes: Mapped[list["ResumeModel"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"<User {self.id} {self.username} {self.email} {self.is_active}>"
