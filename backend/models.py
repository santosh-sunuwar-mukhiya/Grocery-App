from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class UOM(BaseModel):
    uom_id: int
    uom_name: str


class Product(BaseModel):
    product_id: int
    name: str
    uom_id: int
    price_per_unit: float
    uom_name: str


class ProductRequest(BaseModel):
    product_name: str
    uom_id: int
    price_per_unit: float


class OrderDetail(BaseModel):
    product_id: int
    quantity: float
    total_price: float


class OrderDetailResponse(BaseModel):
    order_id: int
    quantity: float
    total_price: float
    product_name: str
    price_per_unit: float


class Order(BaseModel):
    order_id: int
    customer_name: str
    total: float
    datetime: str


class OrderWithDetails(BaseModel):
    order_id: int
    customer_name: str
    total: float
    datetime: str
    order_details: List[OrderDetailResponse]


class OrderRequest(BaseModel):
    customer_name: str
    grand_total: float
    order_details: List[OrderDetail]
