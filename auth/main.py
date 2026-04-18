from contextlib import asynccontextmanager

from fastapi import FastAPI
from auth.api.router import master_router
from auth.databases.session import create_db_tables


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print("....Server Started.....")
    await create_db_tables()
    yield
    print(".....Server Stopped.....")


app = FastAPI(lifespan=lifespan_handler)
app.include_router(master_router)


@app.get("/")
def root():
    return {"message": "Hello World!"}
