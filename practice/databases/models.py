from enum import Enum
from datetime import datetime

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Text

class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


class Shipment(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime

class Seller(SQLModel, table=True):
    id: int = Field(primary_key = True, index=True)
    name: str

    email: EmailStr
    password_hash: str = Field(sa_column=Column(Text))
