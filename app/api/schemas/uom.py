from uuid import UUID
from pydantic import BaseModel


class UOMCreate(BaseModel):
    name: str


class UOMRead(BaseModel):
    id: UUID
    name: str