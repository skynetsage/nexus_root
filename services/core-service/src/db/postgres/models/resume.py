from sqlalchemy import String, Integer, TIMESTAMP, func, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import Optional, List
from datetime import datetime

from ..engine import base

class ResumeTable(base):

    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    resume_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    analysis_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, unique=True)

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(),onupdate=func.now())
    is_analyzed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    files: Mapped["FileTable"] = relationship('FileTable',back_populates="resumes")
    def __repr__(self) -> str:
        return f"<ResumeTable(id={self.id}, resume_id={self.resume_id}, analysis_id={self.analysis_id})>"

