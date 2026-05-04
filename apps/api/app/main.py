"""FastAPI application factory."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan hook. DB pool, Redis, etc. wired in later phases."""
    yield


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="Miroha API",
        description="AI-curated film and series discovery.",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/", tags=["meta"])
    async def root() -> dict[str, str]:
        return {
            "service": "miroha-api",
            "version": "0.1.0",
            "environment": settings.environment,
        }

    return app


app = create_app()
