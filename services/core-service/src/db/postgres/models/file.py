from sqlalchemy import String, Integer, ForeignKey, TIMESTAMP, Boolean, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import Optional, List
from datetime import datetime

from ..engine import base

class FileTable(base):
    __tablename__ = 'files'
    __table_args__ = {'schema': 'public'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    filename: Mapped[str] = mapped_column(String, nullable=True)
    filepath: Mapped[str] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    resume_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey('resumes.resume_id'), nullable=True)

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    users: Mapped[List["UserTable"]] = relationship('UserTable',back_populates="files")
    resumes: Mapped["ResumeTable"] = relationship('ResumeTable',back_populates="files")

    def __repr__(self) -> str:
        return f"<FileTable(id={self.id}, filename={self.filename}, filepath={self.filepath}, is_active={self.is_active})>"

