from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from practice.api.dependencies import SellerServiceDep, SessionDep
from practice.api.schemas.seller import SellerCreate, SellerRead

from practice.core.security import oauth2_scheme
from practice.databases.models import Seller
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


@router.get("/Dashboard")
async def get_dashboard(
    token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep
) -> dict:

    data = decode_access_token(token)

    if data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token."
        )

    seller = await session.get(Seller, data["user"]["id"])

    return {"detail": "Successfully Authenticated.", "user": seller}
