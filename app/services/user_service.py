from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres.models.user_model import User
from app.db.postgres.repository.user_repository import UserRepository
from app.schemas.user_schemas import UserBase
from app.utils.logger import get_logger
from app.utils.password_util import hash_password, verify_password

logger = get_logger("User")


class UserService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.user_repository = UserRepository(db)

    async def sign_up(self, user_data: UserBase) -> tuple[User | None, str | None]:
        existing_user = await self.validate_user(
            user_data.username, user_data.email, user_data.password
        )

        if existing_user:
            logger.debug("Username or email already exists")
            return None, "Username or email already exists"

        user_data.password = hash_password(user_data.password)
        new_user = await self.user_repository.create_user(user_data)
        return new_user, None

    async def login(
        self, username_or_email: str, password: str
    ) -> tuple[User | None, str | None]:
        user = await self.validate_user(username_or_email)
        if not user:
            user = await self.user_repository.get_user_by_username(username_or_email)

        if not user:
            return None, "Invalid username or email"

        if not verify_password(password, user.password):
            return None, "Invalid password"

        return user, None

    async def validate_user(self, username, email, password):
        if (username or email) and password:
            if username and email:
                user = await self.user_repository.verify_user_by_credentials(
                    username, email, password
                )
            elif email:
                user = await self.user_repository.verify_user_by_email(email, password)
            else:
                user = await self.user_repository.verify_user_by_username(
                    username, password
                )
            return user

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.user_repository.get_user_by_id(user_id)

    async def get_user_by_username(self, username: str) -> User | None:
        return await self.user_repository.get_user_by_username(username)

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.user_repository.get_user_by_email(email)

    async def get_all_active_users(self) -> list[User]:
        return await self.user_repository.get_all_active_users()

    async def get_all_inactive_users(self) -> list[User]:
        return await self.user_repository.get_all_inactive_users()

    async def deactivate_user(self, user_id: int) -> User | None:
        return await self.user_repository.delete_user_by_id(user_id)
