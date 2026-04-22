from fastapi import HTTPException, status
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from practice.databases.models import Seller
from practice.databases.redis import is_jti_blacklisted
from practice.databases.session import get_session
from practice.services.seller import SellerService
from practice.services.shipment import ShipmentService
from practice.core.security import oauth2_scheme
from practice.utils import decode_access_token

SessionDep = Annotated[AsyncSession, Depends(get_session)]


# access token dep
async def get_access_token(
    token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep
) -> dict:

    data = decode_access_token(token)

    if data is None or await is_jti_blacklisted(data["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or Expired access token.",
        )

    return data


# Logged in Seller
async def get_current_seller(
    token_data: Annotated[dict, Depends(get_access_token)], session: SessionDep
):
    return await session.get(Seller, token_data["user"]["id"])


def get_shipment_service(session: SessionDep):
    return ShipmentService(session)

def get_seller_service(session: SessionDep):
    return SellerService(session)

SellerDep = Annotated[
    Seller, Depends(get_current_seller)
]  # Current Active Seller Dependencey.

SellerServiceDep = Annotated[
    SellerService, Depends(get_seller_service)
]  # Seller Service Dependencey.

ShipmentServiceDep = Annotated[
    ShipmentService, Depends(get_shipment_service)
]  # Shipment Service Dependency.
