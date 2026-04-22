from redis.asyncio import Redis
from practice.config import db_setting


_token_blacklist = Redis(host=db_setting.REDIS_HOST, port=db_setting.REDIS_PORT, db=1)


async def add_jti_to_blacklist(jti: str):
    await _token_blacklist.set(jti, "blacklisted")


async def is_jti_blacklisted(jti: str) -> bool:
    return await _token_blacklist.exists(jti)
