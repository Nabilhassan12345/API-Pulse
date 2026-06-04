from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl, Field
from services.load_tester import load_tester
from config import settings

router = APIRouter(prefix="/api")

class TestRequest(BaseModel):
    url: HttpUrl
    concurrency: int = Field(ge=1, le=settings.MAX_CONCURRENCY_LIMIT)

@router.post("/start")
async def start_test(request: TestRequest):
    if load_tester.is_running:
        return {"status": "error", "message": "Test is already running"}
    load_tester.start(str(request.url), request.concurrency)
    return {"status": "success", "message": f"Started load test on {request.url}"}

@router.post("/stop")
async def stop_test():
    load_tester.stop()
    return {"status": "success", "message": "Stopped load test"}

@router.get("/status")
async def get_status():
    return {
        "is_running": load_tester.is_running,
        "stats": load_tester.get_stats()
    }
