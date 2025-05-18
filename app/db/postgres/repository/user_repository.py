from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.postgres.models.user_model import UserModel
from app.schemas.user_schema import UserBase


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: int) -> UserModel:
        result = await self.db.execute(
            select(UserModel).where(
                UserModel.id == user_id, UserModel.is_active == True
            )
        )
        return result.scalars().first()

    async def get_user_by_username(self, username: str) -> UserModel:
        result = await self.db.execute(
            select(UserModel).where(
                UserModel.username == username, UserModel.is_active == True
            )
        )
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> UserModel:
        result = await self.db.execute(
            select(UserModel).where(
                UserModel.email == email, UserModel.is_active == True
            )
        )
        return result.scalars().first()

    async def get_all_active_users(self) -> list[UserModel]:
        result = await self.db.execute(
            select(UserModel).where(UserModel.is_active == True)
        )
        return result.scalars().all()

    async def get_all_inactive_users(self) -> list[UserModel]:
        result = await self.db.execute(
            select(UserModel).where(UserModel.is_active == False)
        )
        return result.scalars().all()

    async def delete_user_by_id(self, user_id: int) -> UserModel:
        result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        user_to_deactivate = result.scalars().first()
        if user_to_deactivate:
            user_to_deactivate.is_active = False
            await self.db.commit()
            return user_to_deactivate
        return None

    async def create_user(self, user: UserBase) -> UserModel:
        new_user = UserModel(
            username=user.username,
            email=str(user.email),
            password=user.password,
            is_active=True,
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def verify_user_by_username(
        self, username: str, password: str
    ) -> User | None:
        result = await self.db.execute(
            select(User).where(
                User.username == username,
                User.password == password,
                User.is_active == True,
            )
        )
        return result.scalars().first()

    async def verify_user_by_email(self, email: str, password: str) -> User | None:
        result = await self.db.execute(
            select(User).where(
                User.email == email, password == password, User.is_active == True
            )
        )
        return result.scalars().first()

    async def verify_user_by_credentials(
        self, username: str, email: str, password: str
    ) -> User | None:
        result = await self.db.execute(
            select(User).where(
                User.email == email,
                User.username == username,
                password == password,
                User.is_active == True,
            )
        )
        return result.scalars().first()
