from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from auth.api.schemas.user import UserCreate, UserRead
from auth.api.dependencies import UserServiceDep


router = APIRouter(prefix="/user", tags=["User"])


@router.post("/register", response_model=UserRead)
async def register_user(user_register: UserCreate, service: UserServiceDep):
    return await service.add(user_register)


@router.post("/login")
async def login_user(
    service: UserServiceDep,
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    token = await service.token(request_form.username, request_form.password)

    return {"token": token, "type": "jwt"}
