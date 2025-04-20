from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user_schema import UserBase
from app.services.user_service import UserService
from app.core.logger import get_logger

logger = get_logger("user")


async def register(request: Request, db: AsyncSession):
    data = await request.json()

    required_fields = ["username", "email", "password"]
    if not all(field in data and data[field] for field in required_fields):
        return JSONResponse(
            logger.error("Error creating new user", obj=required_fields, exc_info=True),
            status_code=400,
            content={"error": "Missing required fields"},
        )

    user_data = UserBase(**data)
    user_service = UserService(db)

    new_user, error = await user_service.sign_up(user_data)
    if error:
        return JSONResponse(
            logger.error("Error creating new user", obj=new_user, exc_info=True),
            status_code=400,
            content={"errorMsg": "Error in creating new user", "error": error},
        )
    logger.info("User registered successfully")
    return JSONResponse(
        status_code=201,
        content={"msg": "User registered successfully", "user": new_user.to_dict()},
    )


async def login(request: Request, db: AsyncSession):
    data = await request.json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not (username or email) or not password:
        return JSONResponse(
            status_code=400, content={"error": "Missing username/email or password"}
        )

    user_service = UserService(db)
    user = await user_service.login((username, email), password)

    if not user:
        return JSONResponse(status_code=401, content={"error": "User not found"})

    return JSONResponse(
        status_code=200,
        content={
            "msg": "Login successful",
            "user": user.to_dict(),  # You might want to customize this
        },
    )
