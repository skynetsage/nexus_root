from sqlalchemy.orm import Session
from app.db.models.user_model import User
from app.schemas.user_schemas import UserBase


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def get_user_by_id(self, user_id: int) -> User:
        return (
            self.db.query(User)
            .filter(User.id == user_id, User.is_active == True)
            .first()
        )

    @staticmethod
    def get_user_by_username(self, username: str) -> User:
        return (
            self.db.query(User)
            .filter(User.username == username, User.is_active == True)
            .first()
        )

    @staticmethod
    def get_all_active_users(self) -> list[User]:
        return self.db.query(User).filter(User.is_active == True).all()

    @staticmethod
    def get_all_inactive_users(self) -> list[User]:
        return self.db.query(User).filter(User.is_active == False).all()

    @staticmethod
    def delete_user_by_id(self, user_id: int) -> User:
        user_to_deactivate = self.db.query(User).filter(User.id == user_id).first()
        if user_to_deactivate:
            user_to_deactivate.is_active = False
            self.db.commit()
            return user_to_deactivate

    @staticmethod
    def create_user(self, user: UserBase) -> User:
        new_user = User(
            username=user.username,
            email=str(user.email),
            password=user.password,
            is_active=True,
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
