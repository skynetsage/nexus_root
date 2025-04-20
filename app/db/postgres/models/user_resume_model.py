from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from ..engine import base


class UserResumeModel(base):
    __tablename__ = "user_resume"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    resume_id: Mapped[str] = mapped_column(
        String, ForeignKey("resumes.resume_id"), nullable=False, index=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )

    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, default=func.now()
    )

    # String-based reference to prevent circular import
    resume: Mapped["ResumeModel"] = relationship(
        "ResumeModel", back_populates="user_resumes"
    )
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="user_resumes")

    def __repr__(self) -> str:
        return f"<UserResume user_id={self.user_id} resume_id={self.resume_id}>"
