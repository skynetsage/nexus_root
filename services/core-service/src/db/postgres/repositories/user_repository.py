from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from ..models.user import UserTable
from ....schemas.user import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

class UserRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    async def create_user(self, user_create: UserCreate) -> UserTable:
        """Create a new user record."""
        user_data = user_create.model_dump()
        # Unwrap SecretStr for password
        if hasattr(user_create.password, "get_secret_value"):
            user_data["password"] = user_create.password.get_secret_value()

        db_user = UserTable(**user_data)
        self.db_session.add(db_user)
        await self.db_session.flush()
        await self.db_session.refresh(db_user)
        return db_user


    async def get_user_by_id(self, user_id: int) -> Optional[UserTable]:
        """Get a single user by ID."""
        query = select(UserTable).where(UserTable.id == user_id)
        result = await self.db_session.execute(query)
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> Optional[UserTable]:
        """Get a single user by email."""
        query = select(UserTable).where(UserTable.email == email)
        result = await self.db_session.execute(query)
        return result.scalars().first()

    async def get_user_by_username(self, username: str) -> Optional[UserTable]:
        """Get a single user by email."""
        query = select(UserTable).where(UserTable.username == username)
        result = await self.db_session.execute(query)
        return result.scalars().first()

    async def get_all_users(self, limit: int = 100, offset: int = 0) -> List[UserTable]:
        """Get all users with pagination."""
        query = select(UserTable).offset(offset).limit(limit)
        result = await self.db_session.execute(query)
        return list(result.scalars().all())

    async def get_verified_users(self, limit: int = 100, offset: int = 0) -> List[UserTable]:
        """Get all verified users with pagination."""
        query = (
            select(UserTable)
            .where(UserTable.verified == True)
            .offset(offset)
            .limit(limit)
        )
        result = await self.db_session.execute(query)
        return list(result.scalars().all())

    async def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[UserTable]:
        """Update a user record by ID."""
        db_user = await self.get_user_by_id(user_id)
        if not db_user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)
        if not update_data:
            return db_user

        query = (
            update(UserTable)
            .where(UserTable.id == user_id)
            .values(**update_data)
            .returning(UserTable)
        )
        result = await self.db_session.execute(query)
        updated_user = result.scalars().first()
        if updated_user:
            for key, value in update_data.items():
                setattr(db_user, key, value)
        return db_user

    async def delete_user(self, user_id: int) -> bool:
        """Hard delete a user record by ID."""
        query = delete(UserTable).where(UserTable.id == user_id)
        result = await self.db_session.execute(query)
        return result.rowcount > 0

    async def soft_delete_user(self, user_id: int) -> Optional[UserTable]:
        """Soft delete a user by marking them as unverified."""
        db_user = await self.get_user_by_id(user_id)
        if not db_user:
            return None

        update_data = {"verified": False}
        query = (
            update(UserTable)
            .where(UserTable.id == user_id)
            .values(**update_data)
            .returning(UserTable)
        )
        result = await self.db_session.execute(query)
        updated_user = result.scalars().first()
        if updated_user:
            db_user.verified = False
        return db_user
