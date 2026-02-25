from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.repos.timer_repo import TimerRepository
from app.services.timer_service import TimerService
from app.routers import timers as timers_router

settings = get_settings()

app = FastAPI(title="A cool timers with a Face")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

timer_repo = TimerRepository()
timer_service = TimerService(repo=timer_repo)

timers_router.timer_service = timer_service

app.include_router(timers_router.router)
