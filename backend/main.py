from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import rest, websocket
from config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(rest.router)
app.include_router(websocket.router)
