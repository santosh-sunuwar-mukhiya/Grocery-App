from fastapi import HTTPException, status
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from practice.databases.session import get_session
from practice.services.seller import SellerService
from practice.services.shipment import ShipmentService
from practice.core.security import oauth2_scheme
from practice.utils import decode_access_token

SessionDep = Annotated[AsyncSession, Depends(get_session)]


# access token dep
# def get_access_token(
#     token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep
# ) -> str:

#     data = decode_access_token(token)

#     if data is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token."
#         )


def get_shipment_service(session: SessionDep):
    return ShipmentService(session)

def get_seller_service(session: SessionDep):
    return SellerService(session)

SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]

ShipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]
