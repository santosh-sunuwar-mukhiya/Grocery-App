from uuid import UUID
from fastapi import APIRouter
from app.api.dependencies import OrderServiceDep, UserDep
from app.api.schemas.order import OrderCreate, OrderRead

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=list[OrderRead])
async def get_all_orders(service: OrderServiceDep, _: UserDep):
    return await service.get_all()


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(order_id: UUID, service: OrderServiceDep, _: UserDep):
    return await service.get(order_id)


@router.post("/", response_model=OrderRead)
async def create_order(order: OrderCreate, service: OrderServiceDep, current_user: UserDep):
    return await service.create(order, user_id=current_user.id)