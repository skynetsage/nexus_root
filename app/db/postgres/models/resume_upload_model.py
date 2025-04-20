from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, TIMESTAMP, Integer, ForeignKey
from sqlalchemy.sql import func
from ..engine import base


class ResumeUploadModel(base):
    __tablename__ = "resume_upload"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        index=True,
        unique=True,
    )

    resume_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("resumes.resume_id"),
        nullable=False,
        index=True,
        unique=True,
    )

    filename: Mapped[str] = mapped_column(String, nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    uploaded_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, default=func.now()
    )

    # String-based reference to prevent circular import
    resume: Mapped["ResumeModel"] = relationship(
        "ResumeModel", back_populates="uploads"
    )

    def __repr__(self) -> str:
        return f"<ResumeUpload resume_id={self.resume_id} filename={self.filename}>"
