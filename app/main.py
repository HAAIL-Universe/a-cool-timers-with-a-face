from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import timers
from app.dependencies import get_timer_repo, get_timer_service

app = FastAPI(title="A cool timers with a Face")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(timers.router, prefix="/timers", tags=["timers"])


@app.get("/", tags=["health"])
async def root():
    """Health check endpoint."""
    return {"status": "ok"}


@app.on_event("startup")
async def startup():
    """Initialize singleton instances on startup."""
    get_timer_repo()
    get_timer_service()
