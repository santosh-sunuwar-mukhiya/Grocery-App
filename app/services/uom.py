from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import UOM
from app.api.schemas.uom import UOMCreate
from .base import BaseService


class UOMService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(UOM, session)

    async def get_all(self) -> list[UOM]:
        result = await self.session.execute(select(UOM))
        return list(result.scalars().all())

    async def create(self, data: UOMCreate) -> UOM:
        uom = UOM(**data.model_dump())
        return await self._add(uom)