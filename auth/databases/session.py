from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from auth.config import db_settings

engine = create_async_engine(
    url=db_settings.DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)

AsyncSessionFactory = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def create_db_tables():
    from auth.databases.models import User

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async with AsyncSessionFactory() as session:
        yield session
