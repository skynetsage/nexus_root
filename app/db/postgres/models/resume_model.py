from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from ..engine import base


class ResumeModel(base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False, index=True
    )
    resume_analysis_id: Mapped[UUID | None] = mapped_column(
        UUID, nullable=True, index=True
    )
    resume_id: Mapped[str] = mapped_column(
        String, nullable=False, index=True, unique=True  # Required for FK references
    )
    overall_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    technical_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    grammer_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_analysed: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, default=func.now()
    )
    updated_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    )

    # String-based reference to prevent circular import
    uploads: Mapped[list["ResumeUploadModel"]] = relationship(
        "ResumeUploadModel", back_populates="resume", cascade="all, delete-orphan"
    )

    user_resumes: Mapped[list["UserResumeModel"]] = relationship(
        "UserResumeModel", back_populates="resume", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Resume resume_id={self.resume_id} analysed={self.is_analysed}>"
