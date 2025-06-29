import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from backend.routes import router as api_router, websocket_router
from backend.tasks.scheduler import scheduled_cleanup_task

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages application startup and shutdown events.

    On startup, it launches the background task for room cleanup.
    """
    cleanup_task = asyncio.create_task(scheduled_cleanup_task())
    yield
    cleanup_task.cancel()

def get_app() -> FastAPI:
    """
    Creates and configures the FastAPI application instance.
    """
    app = FastAPI(
        title="The Loom API",
        version="1.0.0",
        lifespan=lifespan
    )
    app.include_router(api_router)
    app.include_router(websocket_router)

    @app.get("/health", tags=["Health Check"])
    def health():
        return {"status": "healthy"}

    return app