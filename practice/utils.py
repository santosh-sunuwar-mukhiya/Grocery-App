from datetime import datetime, timedelta, timezone
from practice.config import security_settings

import jwt

from practice.api.schemas import seller


def generate_access_token(data: dict, expiry: timedelta = timedelta(minutes=15)) -> str:
    return jwt.encode(
        payload={
            **data,
            "exp": datetime.now(timezone.utc) + expiry,
        },
        algorithm=security_settings.JWT_ALGORITHM,
        key=security_settings.JWT_SECRET,
    )


def decode_access_token(token: str) -> dict:
    return jwt.decode(
        jwt=token,
        key=security_settings.JWT_SECRET,
        algorithms=[security_settings.JWT_ALGORITHM],
    )
