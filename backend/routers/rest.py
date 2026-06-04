from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl, Field
from services.load_tester import load_tester
from config import settings
from schemas.scenario import Scenario

router = APIRouter(prefix="/api", tags=["engine"])

@router.post("/start")
async def start_load_test(scenario: Scenario):
    if load_tester.is_running:
        return {"status": "error", "message": "Test is already running"}
    load_tester.start(scenario)
    return {"status": "success", "message": "Load test scenario started"}

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
