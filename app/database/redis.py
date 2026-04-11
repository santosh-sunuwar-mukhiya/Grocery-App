from redis.asyncio import Redis
from app.config import db_settings

# db=0  →  JWT token blacklist (logout)
_token_blacklist = Redis(
    host=db_settings.REDIS_HOST,
    port=db_settings.REDIS_PORT,
    db=0,
)

# db=1  →  product list cache (GET /products)
_product_cache = Redis(
    host=db_settings.REDIS_HOST,
    port=db_settings.REDIS_PORT,
    db=1,
    decode_responses=True,
)

PRODUCT_CACHE_KEY = "all_products"
PRODUCT_CACHE_TTL = 300  # seconds


# ─── Token blacklist helpers ─────────────────────────────────────────────────

async def add_jti_to_blacklist(jti: str) -> None:
    await _token_blacklist.set(jti, "blacklisted")


async def is_jti_blacklisted(jti: str) -> bool:
    return bool(await _token_blacklist.exists(jti))


# ─── Product cache helpers ────────────────────────────────────────────────────

async def get_cached_products() -> str | None:
    return await _product_cache.get(PRODUCT_CACHE_KEY)


async def set_cached_products(data: str) -> None:
    await _product_cache.setex(PRODUCT_CACHE_KEY, PRODUCT_CACHE_TTL, data)


async def invalidate_product_cache() -> None:
    await _product_cache.delete(PRODUCT_CACHE_KEY)