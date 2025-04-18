from app.db.base import Base
from app.db.associations import user_role
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Role(Base):

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, index=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    users = relationship("User", secondary=user_role, back_populates="roles")

    def __repr__(self) -> str:
        return f"<Role {self.id} {self.name} {self.description}>"
