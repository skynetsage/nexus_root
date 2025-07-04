from bson import ObjectId
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from ..db.mongo.mongo import dashboard_data, analysis_data
from ..db.postgres.repositories.user_repository import UserRepository
from ..db.postgres.repositories.resume_repository import ResumeRepository
from ..utils.dashboard_utils import (
    count_scores_overall,
    get_monthly_score_breakdown_from_mongo,
)
from ..utils.mongo_db_utils import convert_mongo_doc_to_json


class DashboardController:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)
        self.resume_repo = ResumeRepository(db)

    async def gen_dashboard_data(self, user_id: int) -> JSONResponse:
        try:
            user_data = await self.user_repo.get_user_by_id(user_id)
            if not user_data:
                raise HTTPException(status_code=404, detail="User not found")

            resume_stats = await self.resume_repo.get_resume_counts_by_user_id(user_id)
            if not resume_stats:
                raise HTTPException(status_code=404, detail="No resumes found for user")

            resume_data = await self.resume_repo.get_all_resumes_by_user_id(user_id)
            if not resume_data:
                raise HTTPException(status_code=404, detail="No resumes found for user")

            overall_counts = await count_scores_overall(resume_data, dashboard_data)
            if overall_counts is None:
                raise HTTPException(
                    status_code=500, detail="Error counting overall scores"
                )

            latest_resume = await self.resume_repo.get_latest_resume_by_user_id(user_id)
            if not latest_resume:
                raise HTTPException(status_code=404, detail="No analyzed resumes found")

            latest_resume_data = await analysis_data.find_one(
                {"_id": ObjectId(latest_resume.analysis_id)}
            )

            if not latest_resume_data:
                raise HTTPException(
                    status_code=404, detail="Latest resume analysis data not found"
                )
            latest_resume_data = convert_mongo_doc_to_json(latest_resume_data)

            monthly_counts, analysis_id_map = (
                await self.resume_repo.get_monthly_resume_counts(user_id)
            )

            monthly_score_breakdown = await get_monthly_score_breakdown_from_mongo(
                analysis_data, analysis_id_map
            )

            monthly_resume_stats = []
            all_months = set(monthly_counts.keys()) | set(
                monthly_score_breakdown.keys()
            )
            for month in sorted(all_months):
                combined = {
                    "month": month,
                    **monthly_counts.get(
                        month, {"total_uploaded": 0, "total_analyzed": 0}
                    ),
                    **monthly_score_breakdown.get(
                        month, {"score_gt_80": 0, "score_lte_80": 0}
                    ),
                }
            monthly_resume_stats.append(combined)

            return JSONResponse(
                content={
                    "user": {
                        "id": user_data.id,
                        "name": user_data.username,
                        "email": user_data.email,
                    },
                    "resume_stats": resume_stats,
                    "overall_counts": overall_counts,
                    "latest_resume": latest_resume_data,
                    "monthly_stats": monthly_resume_stats,  # <-- Added here
                },
                status_code=200,
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while generating dashboard data: {str(e)}",
            )
