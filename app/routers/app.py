from fastapi import APIRouter, Depends
from routers.user import UserRouter

router = APIRouter()

router.include_router(UserRouter, prefix="/user", tags=["User"])


