from fastapi import APIRouter
from auth.api.routers import user

master_router = APIRouter()

master_router.include_router(user.router)
