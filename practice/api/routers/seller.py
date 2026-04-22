from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from practice.api.dependencies import (
    SellerServiceDep,
    SessionDep,
    get_seller_access_token,
)
from practice.api.schemas.seller import SellerCreate, SellerRead

from practice.core.security import oauth2_scheme_seller
from practice.databases.models import Seller
from practice.databases.redis import add_jti_to_blacklist
from practice.utils import decode_access_token

router = APIRouter(prefix="/seller", tags=["Seller"])

@router.post("/signup", response_model=SellerRead)
async def register_seller(seller: SellerCreate, service: SellerServiceDep):
    return await service.add(seller)


@router.post("/token")
async def login_seller(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: SellerServiceDep,
):
    token = await service.token(request_form.username, request_form.password)
    return {
        "access_token": token,  # ✅ Must be this exact key
        "token_type": "bearer",  # ✅ Must be this exact key
    }


@router.get("/logout")
async def logout_seller(
    token_data: Annotated[dict, Depends(get_seller_access_token)],
) -> dict:
    await add_jti_to_blacklist(token_data["jti"])
    return {"detail": "Successfully Logged Out."}
