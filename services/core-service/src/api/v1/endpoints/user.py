from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ....controllers.user_controller import UserController
from ....db.postgres.engine import get_db
from ....schemas.user import UserCreate, UserLogin, UserResponse 

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    controller = UserController(db=db)
    return await controller.signup_user(user_data=user_data)

@user_router.post("/login", response_model=UserResponse)
async def login_user(
    login_data: UserLogin,  #  Use the correct schema
    db: AsyncSession = Depends(get_db)
):
    controller = UserController(db=db)
    return await controller.login_user(login_data=login_data)  # Pass login_data as object
