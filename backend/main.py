import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from load_tester import load_tester

app = FastAPI(title="API-Pulse Backend")

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TestRequest(BaseModel):
    url: str
    concurrency: int

@app.post("/api/start")
async def start_test(request: TestRequest):
    if load_tester.is_running:
        return {"status": "error", "message": "Test is already running"}
    load_tester.start(request.url, request.concurrency)
    return {"status": "success", "message": f"Started load test on {request.url}"}

@app.post("/api/stop")
async def stop_test():
    load_tester.stop()
    return {"status": "success", "message": "Stopped load test"}

@app.get("/api/status")
async def get_status():
    return {
        "is_running": load_tester.is_running,
        "stats": load_tester.get_stats()
    }

@app.websocket("/ws/stats")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = {
                "is_running": load_tester.is_running,
                "stats": load_tester.get_stats()
            }
            await websocket.send_json(data)
            await asyncio.sleep(0.5) # Send updates every 500ms
    except WebSocketDisconnect:
        print("Client disconnected")
