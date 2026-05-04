"""Tests for app.config.Settings."""

import pytest
from pydantic import ValidationError

from app.config import Settings, get_settings


def test_settings_requires_database_urls(monkeypatch: pytest.MonkeyPatch) -> None:
    """Settings must fail loudly if required DB URLs are missing."""
    monkeypatch.delenv("NEON_DATABASE_URL_POOLED", raising=False)
    monkeypatch.delenv("NEON_DATABASE_URL_DIRECT", raising=False)

    with pytest.raises(ValidationError):
        # _env_file=None disables .env loading so the test isn't polluted
        # by the developer's local .env file.
        Settings(_env_file=None)  # type: ignore[call-arg]


def test_settings_loads_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NEON_DATABASE_URL_POOLED", "postgresql://test:test@host/db")
    monkeypatch.setenv("NEON_DATABASE_URL_DIRECT", "postgresql://test:test@host/db")
    monkeypatch.setenv("ENVIRONMENT", "development")

    s = Settings(_env_file=None)  # type: ignore[call-arg]
    assert s.environment == "development"
    assert s.is_development is True
    assert s.is_production is False


def test_cors_origins_split_from_string(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NEON_DATABASE_URL_POOLED", "postgresql://test:test@host/db")
    monkeypatch.setenv("NEON_DATABASE_URL_DIRECT", "postgresql://test:test@host/db")
    monkeypatch.setenv("CORS_ORIGINS", "http://localhost:3000, https://miroha.app")

    s = Settings(_env_file=None)  # type: ignore[call-arg]
    assert "http://localhost:3000" in s.cors_origins
    assert "https://miroha.app" in s.cors_origins


def test_get_settings_is_cached() -> None:
    """get_settings() returns the same instance on repeated calls."""
    get_settings.cache_clear()
    a = get_settings()
    b = get_settings()
    assert a is b
