from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from contextlib import asynccontextmanager

from practice.api.router import router
from practice.databases.session import create_db_tables

@asynccontextmanager
async def lifespan_handler(app: FastAPI):
   await create_db_tables()
   print("Server started and all the tables are created.")
   yield
   print("...Server Stopped and Connection with Tables are closed.")
app = FastAPI(lifespan=lifespan_handler)

app.include_router(router)

### Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )