# Agent guidance — Miroha

This file is read by AI coding agents (Claude Code, Codex) at session start. Follow it strictly. If anything here contradicts a fresh user instruction, ASK before proceeding — do not silently override.

## What we're building

Miroha is a hybrid miroha-first → mass-market movie and web-series discovery platform with an AI Curator that learns user taste and explains every recommendation. India + global, staged: India MVP at week 12, global expansion at week 16. Free-tier infrastructure at MVP scale.

See `PROJECT.md` for current sprint focus. See `ARCHITECTURE.md` for technical design.

## Stack

- **Frontend**: Next.js 14 App Router, TypeScript strict, Tailwind, Framer Motion, React Three Fiber. Hosted on Cloudflare Pages.
- **Backend**: FastAPI on Python 3.12, SQLAlchemy 2.x async, Alembic. Hosted on Fly.io.
- **Database**: Neon Postgres + pgvector. 1024-dim embeddings.
- **Cache**: Upstash Redis.
- **Auth**: Clerk.
- **Background jobs**: Inngest.
- **LLMs (MVP, free tier)**: Gemini 2.5 Flash (primary), Groq Llama 3 (cheap classification), OpenRouter DeepSeek (failover). All calls go through `apps/api/app/llm/router.py`. v1.1 upgrade: Claude Sonnet for Curator chat + explanations.
- **Embeddings**: Jina embeddings v3 (multilingual, 1024-dim, free tier).

## Directory ownership

- `apps/web/` — Next.js frontend
- `apps/api/` — FastAPI backend, including LLM router, recommendation pipeline, Curator memory, ingestion
- `apps/api/app/llm/` — LLM abstraction layer. ALL LLM calls go through here.
- `packages/types/` — Shared TS types (generated from Pydantic)
- `packages/prompts/` — Versioned LLM prompts as markdown files
- `workers/inngest/` — Background functions
- `eval/` — LLM eval harness; run before every prompt change
- `docs/` — Documentation, structured per subfolder

## Architectural commitments (non-negotiable)

These are the design choices that, once changed, cause expensive drift. Never violate these without an ADR.

1. **Single LLM Router**. No code outside `apps/api/app/llm/providers/` may import LLM SDKs (`google.generativeai`, `groq`, `openai`, `anthropic`, etc.). Use the router: `from app.llm.router import LLMRouter`.

2. **Embedding model is fixed at 1024-dim**, currently Jina v3. Changing it requires re-embedding the entire catalog and an ADR.

3. **Prompts live in files, not strings**. Curator prompts, "Why this?" prompts, etc. live in `packages/prompts/*.md`. Code reads them via a loader. This makes prompt changes reviewable.

4. **Repository pattern for DB**. Routers don't query the database directly. Routers call services. Services call repositories. Repositories own SQLAlchemy queries.

5. **Append-mostly interactions table**. Never UPDATE or DELETE rows in `interactions`. Corrections are new rows. The `taste_profiles.taste_vector` is the materialized view.

6. **No PII in URLs**. UUIDs are fine; emails, ratings, names are not.

7. **OTT availability gracefully degrades**. Missing deeplinks fall back to web URLs. Missing availability shows "Check streaming services" instead of erroring.

## Coding conventions

**Python (apps/api)**:
- Python 3.12+, type hints on all public functions
- Pydantic v2 for DTOs and request/response models
- Async by default
- Format with `ruff format`, lint with `ruff check`
- Test with `pytest` + `pytest-asyncio`
- Imports: stdlib, third-party, first-party (`app.*`)

**TypeScript (apps/web)**:
- Strict mode. No `any` without a `// reason:` comment
- Functional components with hooks; no class components
- Tailwind for styling (avoid CSS modules unless animations require)
- Format with `prettier`, lint with `eslint`

**Naming**:
- Files: snake_case (Python), kebab-case (TS)
- Classes: PascalCase
- Functions/vars: snake_case (Python), camelCase (TS)
- Database tables: plural snake_case (`films`, `taste_profiles`)

## Testing rules

- Every router endpoint has at least one happy-path integration test
- Every service that touches LLMs has a unit test with the LLM mocked
- LLM prompt changes require an eval run; never merge without eval results in the PR description
- Migrations have an up-and-down test (apply, rollback, apply)

## Forbidden patterns

- Inline SQL in routers (use repositories)
- LLM SDK imports outside `apps/api/app/llm/providers/`
- Magic strings for OTT platform names — use `ott_platforms.slug`
- Direct manipulation of `taste_profiles.taste_vector` outside the recompute pipeline
- `print()` for logging — use `structlog`
- Storing prompts as Python string literals — use `packages/prompts/*.md`
- Adding fields to `films` for things that aren't intrinsic to the film (user-specific data goes in user-scoped tables)

## When to ask vs. when to proceed

**Ask the user first if**:
- A change requires modifying an architectural commitment above
- A schema change is needed (column add/rename/drop, new table)
- A new external dependency is needed (any library not in `pyproject.toml` or `package.json`)
- An ADR is warranted (anything future-you would want recorded)
- The user's request is ambiguous in a way that affects behavior

**Proceed without asking if**:
- The change is internal to a single module
- It's a refactor with no behavior change
- It's adding tests, fixing a bug with a clear root cause, or documentation

## Decision log

When you make any non-trivial architectural choice (or change one), append an entry to `DECISIONS.md` and create an ADR file in `docs/decisions/NNNN-title.md` using `docs/decisions/template.md`.

## Two-agent coordination (Claude Code + Codex)

This repo is worked on by both Claude Code and Codex. To prevent drift:

1. Both agents read this file. CLAUDE.md and AGENTS.md must stay byte-identical. A pre-commit hook should enforce this.
2. Before starting a session, run `git log --oneline -20` to see what the other agent has been doing.
3. If recent commits look contradictory, STOP and surface to the user.
4. When in doubt about an in-flight feature, check `PROJECT.md` for current focus.
5. Keep commits atomic and descriptive — the other agent's context window is the commit log.

## Sprint focus

Currently in **Phase 0 — repo + governance setup**. See `PROJECT.md` for the current phase and active priorities. Update this when phases change.
