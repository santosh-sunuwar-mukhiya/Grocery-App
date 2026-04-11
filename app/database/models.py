from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlalchemy.dialects import postgresql
from sqlmodel import Column, Field, Relationship, SQLModel


# ─── UOM ─────────────────────────────────────────────────────────────────────

class UOM(SQLModel, table=True):
    __tablename__ = "uom"

    id: UUID = Field(
        sa_column=Column(postgresql.UUID, default=uuid4, primary_key=True)
    )
    name: str = Field(unique=True, index=True)

    products: list["Product"] = Relationship(
        back_populates="uom",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


# ─── Product ──────────────────────────────────────────────────────────────────

class Product(SQLModel, table=True):
    __tablename__ = "product"

    id: UUID = Field(
        sa_column=Column(postgresql.UUID, default=uuid4, primary_key=True)
    )
    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )

    name: str = Field(index=True)
    price_per_unit: float = Field(gt=0)

    uom_id: UUID = Field(foreign_key="uom.id")
    uom: UOM = Relationship(
        back_populates="products",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    order_details: list["OrderDetail"] = Relationship(
        back_populates="product",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


# ─── Order ────────────────────────────────────────────────────────────────────

class Order(SQLModel, table=True):
    __tablename__ = "order"

    id: UUID = Field(
        sa_column=Column(postgresql.UUID, default=uuid4, primary_key=True)
    )
    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )

    customer_name: str
    grand_total: float

    details: list["OrderDetail"] = Relationship(
        back_populates="order",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    # Optional: link order to the user who placed it
    user_id: UUID | None = Field(default=None, foreign_key="user.id")
    user: Optional["User"] = Relationship(
        back_populates="orders",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class OrderDetail(SQLModel, table=True):
    __tablename__ = "order_detail"

    id: UUID = Field(
        sa_column=Column(postgresql.UUID, default=uuid4, primary_key=True)
    )
    quantity: float = Field(gt=0)
    total_price: float = Field(gt=0)

    order_id: UUID = Field(foreign_key="order.id")
    order: Order = Relationship(
        back_populates="details",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    product_id: UUID = Field(foreign_key="product.id")
    product: Product = Relationship(
        back_populates="order_details",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


# ─── User (admin/staff) ───────────────────────────────────────────────────────

class User(SQLModel, table=True):
    __tablename__ = "user"

    id: UUID = Field(
        sa_column=Column(postgresql.UUID, default=uuid4, primary_key=True)
    )
    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )

    name: str
    email: EmailStr = Field(unique=True, index=True)
    email_verified: bool = Field(default=False)
    password_hash: str = Field(exclude=True)  # excluded from serialisation

    orders: list[Order] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"},
    )