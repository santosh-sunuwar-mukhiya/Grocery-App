from sqlalchemy import create_engine
from sqlmodel import SQLModel

engine = create_engine(
    url = "sqlite:///data.db",
    echo = True,
    connect_args = {"check_same_thread":False},
)

def create_db_tables():
    from practice.databases.models import Shipment
    SQLModel.metadata.create_all(bind=engine)