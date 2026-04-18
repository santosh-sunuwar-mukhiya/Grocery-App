from pydantic import EmailStr
from sqlalchemy import Column, Text
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    username: str

    email: EmailStr
    password_hash: str = Field(sa_column=Column(Text))
