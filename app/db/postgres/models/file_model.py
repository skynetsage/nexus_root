from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, TIMESTAMP, Integer, ForeignKey
from sqlalchemy.sql import func
from ..engine import base


class FileUploadModel(base):
    __tablename__ = "file_upload"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True, unique=True
    )
    uploader_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    uploaded_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), nullable=False
    )

    user: Mapped["UserModel"] = relationship(back_populates="uploads")
    resume: Mapped["ResumeModel"] = relationship(
        back_populates="file_upload", uselist=False
    )

    def __repr__(self) -> str:
        return f"<ResumeUpload filename={self.filename}>"
