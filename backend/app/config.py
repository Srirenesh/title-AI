from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    app_name: str = "Verity COS & Title Search API"
    app_env: Literal["development", "test", "production"] = "development"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/verity_title"
    jwt_secret: SecretStr = SecretStr("development-only-change-this-secret-now")
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60
    credential_encryption_key: SecretStr | None = None
    dev_admin_username: str = "admin"
    dev_admin_password: SecretStr = SecretStr("change-me")
    source_mode: Literal["mock", "authorized"] = "mock"
    auto_create_tables: bool = True
    rate_limit_requests: int = Field(default=60, ge=1, le=10_000)
    rate_limit_window_seconds: int = Field(default=60, ge=1, le=3600)
    search_period_years: int = Field(default=40, ge=1, le=100)
    netr_api_key: SecretStr | None = None
    assessor_api_key: SecretStr | None = None
    recorder_api_key: SecretStr | None = None
    court_api_key: SecretStr | None = None
    tax_api_key: SecretStr | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
