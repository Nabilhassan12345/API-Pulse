from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import rest, websocket

app = FastAPI(title="API-Pulse Backend")

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(rest.router)
app.include_router(websocket.router)
