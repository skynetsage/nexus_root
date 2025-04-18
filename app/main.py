from fastapi import FastAPI
from app.api.api_router import api_router
from app.api.v1.endpoints import health
from contextlib import asynccontextmanager

from app.middleware.health_lifespan import HealthCheckMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):

    await health.initialize_health_state(app)

    postgres = "✅ OK" if getattr(app.state, "postgres_healthy", False) else f"❌ {getattr(app.state, 'postgres_error', 'Unknown')}"
    mongo = "✅ OK" if getattr(app.state, "mongo_healthy", False) else f"❌ {getattr(app.state, 'mongo_error', 'Unknown')}"

    print("\n🔍 Health Check at Startup:")
    print(f"  🐘 PostgreSQL: {postgres}")
    print(f"  🍃 MongoDB:    {mongo}\n")

    yield

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
app.add_middleware(HealthCheckMiddleware)