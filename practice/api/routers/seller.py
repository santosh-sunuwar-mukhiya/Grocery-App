from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from practice.api.dependencies import SellerServiceDep
from practice.api.schemas.seller import SellerCreate, SellerRead

from practice.core.security import oauth2_scheme

router = APIRouter(prefix="/seller", tags=["Seller"])

@router.post("/signup", response_model=SellerRead)
async def register_seller(seller: SellerCreate, service: SellerServiceDep):
    return await service.add(seller)

@router.post("/token")
async def login_seller(
        request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
        service: SellerServiceDep
):
    token = await service.token(request_form.username, request_form.password)
    return {
        "token": token,
        "type": "jwt"
    }


@router.get("/Dashboard")
async def get_dashboard(token: Annotated[str, Depends(oauth2_scheme)]):
    return {
        "token": token,
    }
