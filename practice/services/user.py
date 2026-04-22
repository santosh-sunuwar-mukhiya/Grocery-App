from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from practice.databases.models import User
from practice.utils import generate_access_token

from .base import BaseService

_password_hash = PasswordHash((Argon2Hasher(),))


class UserService(BaseService):
    def __init__(self, model: User, session: AsyncSession):
        self.model = model
        self.session = session

    async def _add_user(self, data: dict) -> User:
        user = self.model(
            **data,
            password_hash=_password_hash.hash(data["password"]),
        )  # type: ignore
        return await self._add(user)

    async def _get_by_email(self, email) -> User | None:
        return await self.session.scalar(
            select(self.model).where(self.model.email == email)
        )

    async def _generate_token(self, email, password) -> str:
        # Validate the credentials
        user = await self._get_by_email(email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email or password is incorrect",
            )

        try:
            password_is_correct = _password_hash.verify(password, user.password_hash)
        except Exception:
            # Any error during verification = treat as wrong password
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email or password is incorrect",
            )

        if not password_is_correct:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email or password is incorrect",
            )

        return generate_access_token(
            data={
                "user": {
                    "name": user.name,
                    "id": str(user.id),
                },
            }
        )
