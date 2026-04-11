from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Order, OrderDetail
from app.api.schemas.order import OrderCreate
from .base import BaseService


class OrderService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(Order, session)

    async def get_all(self) -> list[Order]:
        result = await self.session.execute(select(Order))
        return list(result.scalars().all())

    async def get(self, id: UUID) -> Order:
        from fastapi import HTTPException, status
        order = await self._get(id)
        if order is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        return order

    async def create(self, data: OrderCreate, user_id: UUID | None = None) -> Order:
        order = Order(
            customer_name=data.customer_name,
            grand_total=data.grand_total,
            user_id=user_id,
        )
        order = await self._add(order)

        # Insert all order details in one go
        for detail in data.order_details:
            od = OrderDetail(
                order_id=order.id,
                product_id=detail.product_id,
                quantity=detail.quantity,
                total_price=detail.total_price,
            )
            self.session.add(od)

        await self.session.commit()
        await self.session.refresh(order)
        return order