from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from ..engine import base


class ResumeModel(base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    resume_analysis_id: Mapped[UUID | None] = mapped_column(
        UUID, nullable=True, index=True
    )
    resume_id: Mapped[str] = mapped_column(
        String, nullable=False, unique=True, index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    file_id: Mapped[int] = mapped_column(ForeignKey("file_upload.id"), nullable=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), nullable=False
    )
    updated_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user: Mapped["UserModel"] = relationship(back_populates="resumes")
    resume_analysis: Mapped["ResumeAnalysisModel"] = relationship(
        back_populates="resume", uselist=False
    )
    file_upload: Mapped["FileUploadModel"] = relationship(
        back_populates="resume", uselist=False
    )

    def __repr__(self) -> str:
        return f"<Resume resume_id={self.resume_id}>"
