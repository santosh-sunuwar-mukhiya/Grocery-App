from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    id: int
    username: str

class UserRead(UserBase):
    pass

class UserCreate(UserBase):
    email: EmailStr
    password_hashed: str

class UserUpdate(BaseModel):
    username: str | None = Field(default=None)

