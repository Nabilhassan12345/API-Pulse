from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import rest, websocket, health, history
from core.database import init_db
from config import settings
from exceptions import add_exception_handlers
from core.middleware import RequestTracingMiddleware

app = FastAPI(title=settings.PROJECT_NAME)

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_db()

app.add_middleware(RequestTracingMiddleware)

# Register routers
app.include_router(rest.router)
app.include_router(websocket.router)
app.include_router(health.router)
app.include_router(history.router)

# Register exception handlers
add_exception_handlers(app)
