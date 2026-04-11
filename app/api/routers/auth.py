from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.database.redis import add_jti_to_blacklist
from app.api.dependencies import UserServiceDep, get_token_data
from app.api.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=UserRead)
async def signup(user: UserCreate, service: UserServiceDep):
    return await service.register(user.name, user.email, user.password)


@router.post("/token")
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: UserServiceDep,
):
    token = await service.login(form.username, form.password)
    return {"access_token": token, "type": "jwt"}


@router.get("/logout")
async def logout(token_data: Annotated[dict, Depends(get_token_data)]):
    await add_jti_to_blacklist(token_data["jti"])
    return {"detail": "Successfully logged out"}