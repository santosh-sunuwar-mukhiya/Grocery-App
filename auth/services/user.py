from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from auth.api.schemas.user import UserCreate
from auth.databases.models import User
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from auth.config import security_settings

import jwt

_password_hash = PasswordHash((Argon2Hasher(),))


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, user_create: UserCreate):
        user = User(
            **user_create.model_dump(exclude={"password"}),
            password_hash=_password_hash.hash(user_create.password)
        )  # type: ignore

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def token(self, email: EmailStr, password: str):
        result = await self.session.execute(select(User).filter_by(email=email))
        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email or Password is Wrong",
            )

        try:
            password_check = _password_hash.verify(password, user.password_hash)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email or Password is incorrect.",
            )

        if not password_check:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email or Password is incorrect.",
            )

        token = jwt.encode(
            payload={
                "user": {"username": user.username, "email": user.email},
                "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
            },
            algorithm=security_settings.JWT_ALGORITHM,
            key=security_settings.JWT_SECRET,
        )

        return token
