from fastapi import APIRouter, Depends
from routers.user import UserRouter
from routers.auth import AuthRouter

router = APIRouter()

router.include_router(UserRouter, prefix="/user", tags=["User"])
router.include_router(AuthRouter, prefix="/auth", tags=["User"])


