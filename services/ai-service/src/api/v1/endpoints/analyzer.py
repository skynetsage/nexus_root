from fastapi import APIRouter, Request

from ....controllers.resume_controller import ResumeController

resume_analyzer_router = APIRouter(prefix="/resumes")

@resume_analyzer_router.post("/analyze", status_code=200)
async def analyze_resume_endpoint(request: Request):
    data = await request.json()
    resume_id = data.get("resume_id")
    jd = data.get("jd")
    file_path = data.get("file_path")

    if not resume_id or not jd or not file_path:
        return {"error": "Missing required fields: resume_id, jd, file_path"}

    controller = ResumeController()

    result = controller.analyze_resume(file_path, jd, resume_id)
    return result