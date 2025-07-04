from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import SecretStr
from fastapi import HTTPException
from ..schemas.user import UserCreate, UserResponse, UserLogin
from ..db.postgres.repositories.user_repository import UserRepository
# from ..config.logger import get_logger
from ..utils.auth_util import hash_password, verify_password

# logger = get_logger("user")

class UserController:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def signup_user(self, user_data: UserCreate) -> UserResponse:
        try:
            existing_user = await self.user_repo.get_user_by_email(user_data.email)
            if existing_user:
                # logger.warning(f"Signup failed: User with email {user_data.email} already exists")
                raise HTTPException(status_code=400, detail="User with this email already exists")

            hashed_password = hash_password(user_data.password.get_secret_value())
            new_user_data = UserCreate(
                username=user_data.username,
                email=user_data.email,
                password=SecretStr(hashed_password),
                verified=False,
                roles=["user"]
            )
            created_user = await self.user_repo.create_user(new_user_data)
            # logger.info(f"User created successfully with email: {created_user.email}")

            return UserResponse(
                id=created_user.id,
                username=created_user.username,
                email=created_user.email,
                verified=created_user.verified,
                roles=created_user.roles,
                created_at=created_user.created_at,
                updated_at=created_user.updated_at
            )
        except Exception as e:
            # logger.error(f"Error during user signup: {e}")
            raise HTTPException(status_code=500, detail="An error occurred while signing up")

    async def login_user(self, login_data: UserLogin) -> UserResponse:
        try:
            user = await self.user_repo.get_user_by_username(login_data.username)
            if not user:
                # logger.warning(f"Login failed: No user found with email {login_data.email}")
                raise HTTPException(status_code=401, detail="Invalid credentials")

            if not verify_password(login_data.password.get_secret_value(), user.password):
                # logger.warning(f"Login failed: Invalid password for email {login_data.email}")
                raise HTTPException(status_code=401, detail="Invalid credentials")

            # logger.info(f"User logged in successfully: {user.email}")

            return UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                verified=user.verified,
                roles=user.roles,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
        except Exception as e:
            # logger.error(f"Error during user login: {e}")
            raise HTTPException(status_code=500, detail="An error occurred while logging in")
