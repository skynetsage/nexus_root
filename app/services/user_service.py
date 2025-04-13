from app.db.repository.user_repository import UserRepository
from app.schemas.user_schemas import UserBase
from app.utils.password_util import hash_password, verify_password
from app.db.models.user_model import User
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.user_repository = UserRepository(db)

    async def sign_up(self, user_data: UserBase) -> tuple[User | None, str | None]:
        existing_user = await self.user_repository.get_user_by_username(user_data.username)
        existing_email = await self.user_repository.get_user_by_username(user_data.email)

        if existing_user or existing_email:
            return None, "Username or email already exists"

        user_data.password = hash_password(user_data.password)
        new_user = await self.user_repository.create_user(user_data)
        return new_user, None

    async def login(self, username_or_email: str, password: str) -> tuple[User | None, str | None]:
        user = await self.user_repository.get_user_by_username(username_or_email)
        if not user:
            user = await self.user_repository.get_user_by_username(username_or_email)

        if not user:
            return None, "Invalid username or email"

        if not verify_password(password, user.password):
            return None, "Invalid password"

        return user, None

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.user_repository.get_user_by_id(user_id)

    async def get_user_by_username(self, username: str) -> User | None:
        return await self.user_repository.get_user_by_username(username)

    async def get_all_active_users(self) -> list[User]:
        return await self.user_repository.get_all_active_users()

    async def get_all_inactive_users(self) -> list[User]:
        return await self.user_repository.get_all_inactive_users()

    async def deactivate_user(self, user_id: int) -> User | None:
        return await self.user_repository.delete_user_by_id(user_id)
