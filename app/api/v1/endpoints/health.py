from fastapi import APIRouter, Request, status
from app.db.postgres.engine import check_postgres_connection
from app.db.mongodb.engine import check_mongo_connection

db_router = APIRouter(prefix="/health", tags=["db"])

async def initialize_health_state(app):

    postgres_status = await check_postgres_connection()
    mongo_status = await check_mongo_connection()

    if not isinstance(postgres_status, bool) or not postgres_status:
        app.state.postgres_healthy = False
        app.state.postgres_error = postgres_status[1] if isinstance(postgres_status, tuple) else "Unknown error"
    else:
        app.state.postgres_healthy = True

    if not isinstance(mongo_status, bool) or not mongo_status:
        app.state.mongo_healthy = False
        app.state.mongo_error = mongo_status[1] if isinstance(mongo_status, tuple) else "Unknown error"

    else:
        app.state.mongo_healthy = True

@db_router.get("/", status_code=status.HTTP_200_OK)
async def health_check(request: Request):
    health_info = {
        "status": "healthy",
        "databases": {
            "postgres": {
                "status": "online" if request.app.state.postgres_healthy else "offline",
            },
            "mongodb": {
                "status": "online" if request.app.state.mongo_healthy else "offline",
            }
        }
    }

    if not request.app.state.postgres_healthy and hasattr(request.app.state, "postgres_error"):
        health_info["databases"]["postgres"]["error"] = request.app.state.postgres_error

    if not request.app.state.mongo_healthy and hasattr(request.app.state, "mongo_error"):
        health_info["databases"]["mongodb"]["error"] = request.app.state.mongo_error

    if not (request.app.state.postgres_healthy and request.app.state.mongo_healthy):
        health_info["status"] = "degraded"
        return health_info

    return health_info