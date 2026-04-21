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


def decode_access_token(token: str) -> dict | None:
    try:
        print(f"[DEBUG] Decoding token: {token[:30]}...")
        print(f"[DEBUG] Secret being used: {security_settings.JWT_SECRET}")
        print(f"[DEBUG] Algorithm: {security_settings.JWT_ALGORITHM}")
        return jwt.decode(
            jwt=token,
            key=security_settings.JWT_SECRET,
            algorithms=[security_settings.JWT_ALGORITHM],
        )
    except Exception as e:  # ← catch ALL exceptions temporarily
        print(f"[DEBUG] Error type: {type(e).__name__}")
        print(f"[DEBUG] Error message: {e}")
        print(f"[DEBUG] Received token:  '{token}'")
        print(f"[DEBUG] Received length: {len(token)}")
        return None
