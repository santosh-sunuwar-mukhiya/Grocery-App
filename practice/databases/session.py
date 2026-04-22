from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from practice.config import db_setting

engine = create_async_engine(
    url = db_setting.POSTGRES_URL,
    echo = True,
)

AsyncSessionFactory = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False  # type: ignore
)  # type: ignore

from practice.databases.models import Shipment, Seller

async def create_db_tables():
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async with AsyncSessionFactory() as session:  # type: ignore
        yield session
