from uuid import UUID
from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str
    price_per_unit: float = Field(gt=0)
    uom_id: UUID


class ProductUpdate(BaseModel):
    name: str | None = None
    price_per_unit: float | None = Field(default=None, gt=0)
    uom_id: UUID | None = None


class ProductRead(BaseModel):
    id: UUID
    name: str
    price_per_unit: float
    uom_id: UUID