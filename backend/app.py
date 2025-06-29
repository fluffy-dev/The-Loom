import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import router as api_router, websocket_router
from backend.tasks.scheduler import scheduled_cleanup_task
from backend.logging_setup import setup_logging
from backend.handlers import exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages application startup and shutdown events.
    """
    cleanup_task = asyncio.create_task(scheduled_cleanup_task())
    yield
    cleanup_task.cancel()

def get_app() -> FastAPI:
    """
    Creates and configures the FastAPI application instance.
    """
    # Инициализируем логирование при старте
    setup_logging()
    app = FastAPI(
        title="The Loom API",
        version="1.0.0",
        lifespan=lifespan,
        exception_handlers=exception_handlers # <-- Регистрируем обработчики
    )

    # Настраиваем CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # В продакшене укажите конкретные домены
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)
    app.include_router(websocket_router)

    @app.get("/health", tags=["Health Check"])
    def health():
        return {"status": "healthy"}

    return app