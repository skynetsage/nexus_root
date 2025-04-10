from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user_model import User
from app.schemas.user_schemas import UserBase


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: int) -> User | None:
        return (
            await self.db.query(User)
            .filter(User.id == user_id, User.is_active == True)
            .first()
        )

    async def get_user_by_username(self, username: str) -> User | None:
        return (
            await self.db.query(User)
            .filter(User.username == username, User.is_active == True)
            .first()
        )

    async def get_all_active_users(self) -> list[User]:
        return await self.db.query(User).filter(User.is_active == True).all()

    async def get_all_inactive_users(self) -> list[User]:
        return await self.db.query(User).filter(User.is_active == False).all()

    async def delete_user_by_id(self, user_id: int) -> User | None:
        user_to_deactivate = (
            await self.db.query(User).filter(User.id == user_id).first()
        )
        if user_to_deactivate:
            user_to_deactivate.is_active = False
            await self.db.commit()
            return user_to_deactivate
        return None

    async def create_user(self, user: UserBase) -> User:
        new_user = User(
            username=user.username,
            email=str(user.email),
            password=user.password,
            is_active=True,
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user
