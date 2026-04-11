from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import oauth2_scheme
from app.database.models import User
from app.database.redis import is_jti_blacklisted
from app.database.session import get_session
from app.services.product import ProductService
from app.services.order import OrderService
from app.services.uom import UOMService
from app.services.user import UserService
from app.utils import decode_access_token

# ─── DB session ───────────────────────────────────────────────────────────────
SessionDep = Annotated[AsyncSession, Depends(get_session)]


# ─── Auth ─────────────────────────────────────────────────────────────────────

async def get_token_data(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    data = decode_access_token(token)
    if data is None or await is_jti_blacklisted(data["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
        )
    return data


async def get_current_user(
    token_data: Annotated[dict, Depends(get_token_data)],
    session: SessionDep,
) -> User:
    user = await session.get(User, UUID(token_data["user"]["id"]))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    return user


UserDep = Annotated[User, Depends(get_current_user)]


# ─── Service factories ────────────────────────────────────────────────────────

def get_user_service(session: SessionDep) -> UserService:
    return UserService(session)


def get_product_service(session: SessionDep) -> ProductService:
    return ProductService(session)


def get_order_service(session: SessionDep) -> OrderService:
    return OrderService(session)


def get_uom_service(session: SessionDep) -> UOMService:
    return UOMService(session)


UserServiceDep    = Annotated[UserService,    Depends(get_user_service)]
ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]
OrderServiceDep   = Annotated[OrderService,   Depends(get_order_service)]
UOMServiceDep     = Annotated[UOMService,     Depends(get_uom_service)]