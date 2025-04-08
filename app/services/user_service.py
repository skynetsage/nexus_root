from sqlalchemy.orm import Session
from app.db.repository.user_repository import UserRepository
from app.schemas.user_schemas import UserBase, UserOut
from app.utils.password_util import hash_password


class UserService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.user_repository = UserRepository(db)

    @staticmethod
    def sign_up(self, user_data: UserBase):

        if self.user_repository.get_user_by_email(user_data.email):
            raise ValueError("Username already exists")
        user_data.password = hash_password(user_data.password)
        return self.user_repository.create_user(user_data)
