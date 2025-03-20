from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"
    SECRET_KEY: SecretStr = SecretStr("Life is like a box of chocolates...")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    OPENAI_API_KEY: SecretStr
    API_TOKEN_BYTES: int = 32
    ENV: str = Field("dev", validation_alias="ENV")  # 使用 validation_alias 替代 env

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()