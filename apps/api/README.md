# Miroha API

FastAPI backend for Miroha — film catalog, recommendations, Curator chat, ingestion pipeline.

## Quick start (local)

Prerequisites: Python 3.12+, `uv` (Astral's package manager).

    cd apps/api
    uv sync                # install dependencies into .venv
    uv run uvicorn app.main:app --reload --port 8000

Open `http://localhost:8000/docs` for the OpenAPI explorer.

## Layout

- `app/` — application code
  - `main.py` — FastAPI app factory
  - `routers/` — HTTP routes (thin)
  - `services/` — business logic
  - `llm/` — LLM router and providers
  - `models/` — Pydantic + SQLAlchemy
  - `db/` — DB session, Alembic
- `tests/` — pytest suite
- `alembic/` — DB migrations

See `/ARCHITECTURE.md` and `/CLAUDE.md` at the repo root for conventions.
