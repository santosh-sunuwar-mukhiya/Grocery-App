from uuid import UUID
from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.utils import generate_access_token
from .base import BaseService

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _truncate_password(password: str) -> str:
    """Safely truncate password to 72 bytes for passlib bcrypt."""
    return password.encode("utf-8")[:72].decode("utf-8", "ignore")


class UserService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def register(self, name: str, email: str, password: str) -> User:
        # Check email uniqueness
        existing = await self.session.scalar(
            select(User).where(User.email == email)
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )
        user = User(
            name=name,
            email=email,
            password_hash=password_context.hash(_truncate_password(password)),
            email_verified=True,   # simplified: no email step needed for admin
        )
        return await self._add(user)

    async def login(self, email: str, password: str) -> str:
        user = await self.session.scalar(
            select(User).where(User.email == email)
        )
        if user is None or not password_context.verify(_truncate_password(password), user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email or password is incorrect",
            )
        return generate_access_token(
            data={"user": {"id": str(user.id), "name": user.name}}
        )