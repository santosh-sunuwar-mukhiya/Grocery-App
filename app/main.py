from contextlib import asynccontextmanager
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.api.router import master_router
from app.database.session import create_db_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (use Alembic in production)
    await create_db_tables()
    yield


app = FastAPI(title="Grocery Store API", lifespan=lifespan)
app.include_router(master_router)


@app.get("/scalar", include_in_schema=False)
def scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Grocery API")