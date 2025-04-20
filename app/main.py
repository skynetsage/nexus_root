from fastapi import FastAPI
from app.api.api_router import api_router
from app.api.v1.endpoints import health
from contextlib import asynccontextmanager

from app.middleware.health_lifespan import HealthCheckMiddleware
from app.middleware.logger_middleware import HTTPLoggerMiddleware
from app.db.postgres.engine import initialize_table


@asynccontextmanager
async def lifespan(app: FastAPI):

    await health.initialize_health_state(app)
    await initialize_table()

    postgres = (
        "✅ OK"
        if getattr(app.state, "postgres_healthy", False)
        else f"❌ {getattr(app.state, 'postgres_error', 'Unknown')}"
    )
    mongo = (
        "✅ OK"
        if getattr(app.state, "mongo_healthy", False)
        else f"❌ {getattr(app.state, 'mongo_error', 'Unknown')}"
    )

    print("\n🔍 Health Check at Startup:")
    print(f"  🐘 PostgreSQL: {postgres}")
    print(f"  🍃 MongoDB:    {mongo}\n")

    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(HTTPLoggerMiddleware)
app.add_middleware(HealthCheckMiddleware)

app.include_router(api_router)
