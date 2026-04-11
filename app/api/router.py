from fastapi import APIRouter
from .routers import auth, products, orders, uom

master_router = APIRouter()
master_router.include_router(auth.router)
master_router.include_router(uom.router)
master_router.include_router(products.router)
master_router.include_router(orders.router)