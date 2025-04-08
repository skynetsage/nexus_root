from app.db.base import Base
from app.db.associations import user_role
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
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    roles = relationship("Role", secondary=user_role, back_populates="users")
    otps = relationship("OTP", back_populates="user")

    def __repr__(self) -> str:
        return f"<User {self.id} {self.username} {self.email} {self.is_active} {self.created_at} {self.updated_at}>"
