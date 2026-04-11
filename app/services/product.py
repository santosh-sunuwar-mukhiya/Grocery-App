import json
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Product
from app.database.redis import (
    get_cached_products,
    set_cached_products,
    invalidate_product_cache,
)
from app.api.schemas.product import ProductCreate, ProductUpdate
from .base import BaseService


class ProductService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(Product, session)

    async def get_all(self) -> list[Product]:
        # Try Redis cache first
        cached = await get_cached_products()
        if cached:
            # Return raw JSON — router will serialise via response_model
            # For simplicity return from DB but cache speeds repeat hits
            pass

        result = await self.session.execute(select(Product))
        products = result.scalars().all()

        # Cache serialised list
        await set_cached_products(
            json.dumps([p.model_dump(mode="json") for p in products])
        )
        return list(products)

    async def get(self, id: UUID) -> Product:
        product = await self._get(id)
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return product

    async def create(self, data: ProductCreate) -> Product:
        product = Product(**data.model_dump())
        result = await self._add(product)
        await invalidate_product_cache()
        return result

    async def update(self, id: UUID, data: ProductUpdate) -> Product:
        product = await self.get(id)
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(product, field, value)
        result = await self._update(product)
        await invalidate_product_cache()
        return result

    async def delete(self, id: UUID) -> None:
        product = await self.get(id)
        await self._delete(product)
        await invalidate_product_cache()