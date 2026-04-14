from pydantic_settings import BaseSettings, SettingsConfigDict

_base_config = SettingsConfigDict(
    env_file="./.env",
    env_ignore_empty=True,
    extra="ignore",
)

class Setting(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT:int
    POSTGRES_USERNAME:str
    POSTGRES_PASSWORD: str
    POSTGRES_DB:str

    model_config = _base_config

    @property
    def POSTGRES_URL(self):
        # postgres_url = "postgresql+asyncpg://username:password@host:port/db_name"
        return f"postgresql+asyncpg://{self.POSTGRES_USERNAME}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

db_setting = Setting()
print(db_setting.POSTGRES_URL)