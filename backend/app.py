from fastapi import FastAPI
from backend.routes import router as api_router, websocket_router


def get_app() -> FastAPI:
    """
    Creates and configures the FastAPI application instance.
    """
    app = FastAPI(
        title="The Loom API",
        version="1.0.0",
    )
    app.include_router(api_router)
    app.include_router(websocket_router)

    @app.get("/health", tags=["Health Check"])
    def health():
        return {"status": "healthy"}

    return app