import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.load_tester import load_tester

router = APIRouter(prefix="/ws")

@router.websocket("/stats")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = {
                "is_running": load_tester.is_running,
                "stats": load_tester.get_stats()
            }
            await websocket.send_json(data)
            await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        print("Client disconnected from WebSocket")
