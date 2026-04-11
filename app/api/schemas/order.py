from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class OrderDetailCreate(BaseModel):
    product_id: UUID
    quantity: float = Field(gt=0)
    total_price: float = Field(gt=0)


class OrderDetailRead(BaseModel):
    product_id: UUID
    quantity: float
    total_price: float


class OrderCreate(BaseModel):
    customer_name: str = Field(min_length=1)
    grand_total: float = Field(gt=0)
    order_details: list[OrderDetailCreate] = Field(min_length=1)


class OrderRead(BaseModel):
    id: UUID
    customer_name: str
    grand_total: float
    created_at: datetime
    details: list[OrderDetailRead]