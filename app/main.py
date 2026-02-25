from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import timers
from app.config import get_settings

app = FastAPI(title="A cool timers with a Face", version="0.1.0")

settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(timers.router)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
