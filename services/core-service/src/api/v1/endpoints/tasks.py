from celery import shared_task

@shared_task
def resume_analysis_task(user_id: int, resume_id: str, jd: str):
    from ....db.postgres.engine import async_session_maker
    from ....controllers.resume_controller import ResumeController
    import asyncio

    async def run():
        async with async_session_maker() as db:
            controller = ResumeController(db=db)
            result = await controller.resume_analyze(
                user_id=user_id,
                resume_id=resume_id,
                jd=jd,
            )
            return result

    return asyncio.run(run())
