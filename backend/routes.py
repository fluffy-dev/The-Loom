from fastapi import APIRouter
from backend.user.router import router as user_router

router = APIRouter(prefix="/api")
router.include_router(user_router)