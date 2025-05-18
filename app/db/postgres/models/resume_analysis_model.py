from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from ..engine import base


class ResumeAnalysisModel(base):
    __tablename__ = "resume_analysis"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    resume_id: Mapped[str] = mapped_column(
        ForeignKey("resumes.resume_id"), nullable=False, index=True
    )
    collection_id: Mapped[str] = mapped_column(String(24), nullable=True)
    overall_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    technical_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    grammar_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_analysed: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), nullable=False
    )
    updated_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    resume: Mapped["ResumeModel"] = relationship(back_populates="resume_analysis")

    def __repr__(self) -> str:
        return f"<ResumeAnalysis resume_id={self.resume_id} overall_score={self.overall_score}>"
