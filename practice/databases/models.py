from enum import Enum
from datetime import datetime

from pydantic import EmailStr
from sqlmodel import Relationship, SQLModel, Field, Column
from sqlalchemy import Text
from sqlalchemy.dialects import postgresql

from uuid import uuid4, UUID

class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


class Shipment(SQLModel, table=True):
    id: UUID = Field(sa_column=Column(postgresql.UUID, default=uuid4, primary_key=True))
    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime

    seller_id: UUID = Field(foreign_key="seller.id")
    seller: "Seller" = Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

class Seller(SQLModel, table=True):
    id: UUID = Field(sa_column=Column(postgresql.UUID, default=uuid4, primary_key=True))
    name: str
    address: int
    email: EmailStr
    password_hash: str = Field(sa_column=Column(Text))

    shipments: list[Shipment] = Relationship(
        back_populates="seller",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
