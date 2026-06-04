from fastapi import APIRouter
from pydantic import BaseModel
from services.load_tester import load_tester

router = APIRouter(prefix="/api")

class TestRequest(BaseModel):
    url: str
    concurrency: int

@router.post("/start")
async def start_test(request: TestRequest):
    if load_tester.is_running:
        return {"status": "error", "message": "Test is already running"}
    load_tester.start(request.url, request.concurrency)
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
