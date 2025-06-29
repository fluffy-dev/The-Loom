from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.config.database.engine import db_helper
from app.config.database.settings import settings
from app.database.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages application startup and shutdown events.

    On startup, it optionally creates database tables based on the
    `DB_RUN_AUTO_MIGRATE` setting.
    On shutdown, it disposes of the database engine connections.
    """
    yield
    await db_helper.engine.dispose()


app = FastAPI(
    title="The Loom API",
    description="API for the real-time collaboration platform 'The Loom'.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/", tags=["Health Check"])
async def root():
    """
    A simple health check endpoint.

    Returns:
        dict: A status message indicating the API is running.
    """
    return {"status": "ok", "message": "Welcome to The Loom API!"}

# Routers for different domains (like 'user') will be included here later.