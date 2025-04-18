from app.db.base import Base
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone


class OTP(Base):

    __tablename__ = "otps"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, index=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    otp_code: Mapped[str] = mapped_column(String(6), nullable=False)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(timezone.utc)
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    user = relationship("User", back_populates="otps")

    def __repr__(self) -> str:
        return f"<OTP {self.id} {self.user_id} {self.otp_code} {self.is_used} {self.created_at} {self.expires_at}>"
