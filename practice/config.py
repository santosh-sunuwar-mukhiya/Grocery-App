from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from pydantic import field_validator

_base_config = SettingsConfigDict(
    env_file=Path(__file__).parent / ".env",
    env_ignore_empty=True,
    extra="ignore",
)

class Setting(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT:int
    POSTGRES_USERNAME:str
    POSTGRES_PASSWORD: str
    POSTGRES_DB:str

    REDIS_HOST: str
    REDIS_PORT: int

    model_config = _base_config

    @property
    def POSTGRES_URL(self):
        # postgres_url = "postgresql+asyncpg://username:password@host:port/db_name"
        return f"postgresql+asyncpg://{self.POSTGRES_USERNAME}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

class SecuritySettings(BaseSettings):
    JWT_SECRET: str
    JWT_ALGORITHM: str

    model_config = _base_config

    @field_validator("JWT_SECRET")
    @classmethod
    def secret_must_be_strong(cls, v: str) -> str:
        if len(v.encode()) < 32:
            raise ValueError(
                f"JWT_SECRET is {len(v.encode())} bytes — must be at least 32 bytes. "
                'Run: python -c "import secrets; print(secrets.token_hex(32))"'
            )
        return v


db_setting = Setting()
security_settings = SecuritySettings()
