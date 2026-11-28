"""Configuration from environment variables, validated at startup (PY-021)."""

from __future__ import annotations

from pydantic import Field, HttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings of the service. Every variable starts with `QA_`; see `.env.example`."""

    model_config = SettingsConfigDict(env_prefix="QA_", env_file=".env", extra="ignore")

    max_documents: int = Field(default=3, ge=1, le=10)
    llm_base_url: HttpUrl | None = None
    llm_api_key: SecretStr | None = None
    llm_model: str = "mistral-small-latest"
    llm_timeout_seconds: float = Field(default=20.0, gt=0)
