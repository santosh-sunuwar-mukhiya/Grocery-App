from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
import jwt
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from practice.api.schemas.seller import SellerCreate
from practice.config import security_settings
from practice.databases.models import Seller

from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
_password_hash = PasswordHash((Argon2Hasher(),))

class SellerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, seller_create: SellerCreate) -> Seller:
        seller = Seller(
            **seller_create.model_dump(exclude=["password"]),

            password_hash = _password_hash.hash(seller_create.password),
        )

        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)

        return seller

    async def token(self, email: EmailStr, password) -> str:
        result = await self.session.execute(
            select(Seller).where(Seller.email == email)
        )
        seller = result.scalar()

        if seller is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email or Password is incorrect.",
            )

        try:
            password_is_correct = _password_hash.verify(password, seller.password_hash)
        except Exception:
            # Any error during verification = treat as wrong password
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email or Password is incorrect.",
            )

        if not password_is_correct:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email or Password is incorrect.",
            )

        token = jwt.encode(
            payload = {
                "user": {
                    "name": seller.name,
                    "email": seller.email,
                },
                "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
            },
            algorithm=security_settings.JWT_ALGORITHM,
            key=security_settings.JWT_SECRET,
        )

        return token

