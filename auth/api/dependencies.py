from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.databases.session import get_session
from auth.services.user import UserService


sessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_user_service(session: sessionDep):
    return UserService(session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
