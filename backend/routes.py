from fastapi import APIRouter
from backend.user.router import router as user_router
from backend.auth.router import router as auth_router
from backend.room.router import router as room_router


router = APIRouter(prefix="/api")


router.include_router(auth_router)
router.include_router(user_router)
router.include_router(room_router)