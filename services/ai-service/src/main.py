import sys
from pathlib import Path
import os

# current_file_directory = os.path.dirname(os.path.abspath(__file__))
#
# core_service_src_path = os.path.join(current_file_directory, '..', '..', 'core-service', 'src')
# core_service_src_path = os.path.abspath(core_service_src_path) # Normalize to an absolute path
#
# if core_service_src_path not in sys.path:
#     sys.path.append(core_service_src_path)
# Set up paths using pathlib (more reliable than os.path)
current_file_path = Path(__file__).resolve()
core_service_src_path = current_file_path.parent.parent.parent / "core-service" / "src"

# Add to Python path if not already present
if str(core_service_src_path) not in sys.path:
    sys.path.insert(0, str(core_service_src_path))
    # logger.info(f"Added to sys.path: {core_service_src_path}")
from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    from .api.v1.api_router import api_router

    app.include_router(api_router)  # Adjust prefix as needed

    @app.get("/")
    async def root():
        return {"message": "Welcome to the AI Service"}

    return app


app = create_app()
