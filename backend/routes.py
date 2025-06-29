from fastapi import APIRouter
from backend.user.router import router as user_router
from backend.auth.router import router as auth_router
from backend.room.router import router as room_router
from backend.collaboration.router import router as collaboration_router


router = APIRouter(prefix="/api")


router.include_router(auth_router)
router.include_router(user_router)
router.include_router(room_router)

websocket_router = APIRouter()

websocket_router.include_router(collaboration_router)