from fastapi import FastAPI
from app.routes.user_routes import register_auth_routes
from fastapi import Request
from fastapi.responses import JSONResponse
import traceback
app = FastAPI()

register_auth_routes(app)

@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": f"Unexpected error: {str(exc)}"},
    )



@app.get("/")
def read_root():
    return {"msg": "Welcome to the backend!"}
