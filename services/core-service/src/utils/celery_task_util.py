import asyncio
from httpx import AsyncClient

from ..config.settings import settings

# ensure we use async version of httpx for Celery subprocess
def run_analysis_task(resume_id: str, jd: str, file_path: str) -> dict:
    async def _make_request():
        async with AsyncClient(timeout=300.0) as client:
            response = await client.post(
                url=settings.AI_SERVICE_URL,
                json={"resume_id": resume_id, "jd": jd, "file_path": file_path},
            )
            response.raise_for_status()
            return response.json()

    return asyncio.run(_make_request())
