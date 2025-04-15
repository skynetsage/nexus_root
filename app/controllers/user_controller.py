from fastapi import Request
from fastapi.responses import JSONResponse
from app.schemas.user_schemas import UserBase
from app.services.user_service import UserService
from sqlalchemy.ext.asyncio import AsyncSession


async def register(request: Request, db: AsyncSession):
    data = await request.json()

    required_fields = ["username", "email", "password"]
    if not all(field in data and data[field] for field in required_fields):
        return JSONResponse(status_code=400, content={"error": "Missing required fields"})

    user_data = UserBase(**data)
    user_service = UserService(db)

    new_user, error = await user_service.sign_up(user_data)
    if error:
        return JSONResponse(status_code=400, content={"errorMsg":"Error in creating new user","error": error})

    return JSONResponse(
        status_code=201,
        content={"msg": "User registered successfully", "user": new_user.to_dict()},
    )


async def login(request: Request, db: AsyncSession):
    data = await request.json()

    username = data.get("username") 
    email  = data.get("email")
    password = data.get("password")

    if not (username or email)  or not password:
        return JSONResponse(
            status_code=400, content={"error": "Missing username/email or password"}
        )

    user_service = UserService(db)
    user = await user_service.login((username,email), password)

    if not user:
        return JSONResponse(status_code=401, content={"error": "User not found"})

    return JSONResponse(
        status_code=200,
        content={
            "msg": "Login successful",
            "user": user.to_dict(),  # You might want to customize this
        },
    )
