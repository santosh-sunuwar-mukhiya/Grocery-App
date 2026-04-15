from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from practice.api.schemas.shipment import ShipmentCreate, ShipmentUpdate
from practice.databases.models import Shipment, ShipmentStatus


class ShipmentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Shipment:
        return await self.session.get(Shipment, id)

    async def add(self, shipment_create: ShipmentCreate) -> Shipment:
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now() + timedelta(days=3)
        )

        self.session.add(new_shipment)
        await self.session.commit()
        await self.session.refresh(new_shipment)
        # Return id for later use
        return new_shipment

    async def update(self, id: int, shipment_update: ShipmentUpdate) -> ShipmentUpdate:
        shipment = await self.session.get(Shipment, id)

        if not shipment:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Shipment with #{shipment} does not exist."
            )

        shipment.sqlmodel_update(shipment_update)
        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)

        return shipment

    async def delete(self, id: int):
        shipment = await self.session.get(Shipment, id)

        if not shipment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shipment not found"
            )
        await self.session.delete(shipment)
        await self.session.commit()


