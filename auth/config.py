from pydantic_settings import BaseSettings, SettingsConfigDict

_base_config = SettingsConfigDict(
    env_file="./.env", env_ignore_empty=True, extra="ignore"
)


class DatabaseSetting(BaseSettings):
    DATABASE_URL: str

    model_config = _base_config


class SecuritySetting(BaseSettings):
    JWT_ALGORITHM: str
    JWT_SECRET: str

    model_config = _base_config


db_settings = DatabaseSetting()  # type: ignore
security_settings = SecuritySetting()  # type: ignore

print(db_settings.DATABASE_URL)
