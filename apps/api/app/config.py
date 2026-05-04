"""Typed application configuration.

All env access in the codebase goes through `get_settings()`. Never call
os.getenv directly outside this module. Required fields fail loudly at
startup if missing — no silent None defaults.
"""

from functools import lru_cache
from typing import Annotated, Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ─── Environment ────────────────────────────────────────────────
    environment: Literal["development", "staging", "production"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    # ─── Database (Neon) ────────────────────────────────────────────
    # Pooled URL for the FastAPI runtime; direct URL for Alembic migrations.
    database_url_pooled: SecretStr = Field(..., alias="NEON_DATABASE_URL_POOLED")
    database_url_direct: SecretStr = Field(..., alias="NEON_DATABASE_URL_DIRECT")

    # ─── Cache (Upstash Redis) ──────────────────────────────────────
    # Optional at this stage; required from Phase 3 onward.
    redis_url: SecretStr | None = Field(default=None, alias="REDIS_URL")

    # ─── Auth (Clerk) ───────────────────────────────────────────────
    clerk_publishable_key: SecretStr | None = Field(default=None, alias="CLERK_PUBLISHABLE_KEY")
    clerk_secret_key: SecretStr | None = Field(default=None, alias="CLERK_SECRET_KEY")

    # ─── LLM providers ──────────────────────────────────────────────
    gemini_api_key: SecretStr | None = Field(default=None, alias="GEMINI_API_KEY")
    groq_api_key: SecretStr | None = Field(default=None, alias="GROQ_API_KEY")
    openrouter_api_key: SecretStr | None = Field(default=None, alias="OPENROUTER_API_KEY")
    anthropic_api_key: SecretStr | None = Field(default=None, alias="ANTHROPIC_API_KEY")
    openai_api_key: SecretStr | None = Field(default=None, alias="OPENAI_API_KEY")

    # ─── Embeddings ─────────────────────────────────────────────────
    jina_api_key: SecretStr | None = Field(default=None, alias="JINA_API_KEY")

    # ─── External APIs ──────────────────────────────────────────────
    tmdb_api_key: SecretStr | None = Field(default=None, alias="TMDB_API_KEY")
    tmdb_read_access_token: SecretStr | None = Field(default=None, alias="TMDB_READ_ACCESS_TOKEN")

    # ─── Telemetry ──────────────────────────────────────────────────
    sentry_dsn: SecretStr | None = Field(default=None, alias="SENTRY_DSN")
    posthog_api_key: SecretStr | None = Field(default=None, alias="POSTHOG_API_KEY")
    posthog_host: str = Field(default="https://app.posthog.com", alias="POSTHOG_HOST")

    # ─── CORS ───────────────────────────────────────────────────────
    # NoDecode disables pydantic-settings' JSON pre-parsing so the raw
    # comma-separated env string reaches our split_cors validator.
    cors_origins: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: ["http://localhost:3000"]
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_cors(cls, v: object) -> object:
        """Allow CORS_ORIGINS to be a comma-separated string in env."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    # ─── Helpers ────────────────────────────────────────────────────
    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        return self.environment == "development"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached Settings instance.

    Cached so we parse .env exactly once per process. Tests can call
    get_settings.cache_clear() to force a reload after env changes.
    """
    return Settings()  # type: ignore[call-arg]
