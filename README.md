# Miroha

An AI-powered movie and web-series discovery platform with a personal Curator that learns your taste, finds what to watch across every streaming service, and explains why every recommendation makes sense for you.

**Status**: Pre-MVP. India + global launch staged: India MVP at week 12, global expansion at week 16.

## What's here

- `apps/web/` — Next.js 14 frontend (Cloudflare Pages)
- `apps/api/` — FastAPI backend (Fly.io)
- `packages/` — Shared types and prompts
- `workers/inngest/` — Background jobs
- `eval/` — LLM eval harness
- `docs/` — Documentation (start at `docs/onboarding/SETUP.md`)
- `infra/` — Deployment configuration

## Key documents

- `PROJECT.md` — Product context, current sprint focus
- `ARCHITECTURE.md` — Technical architecture
- `DECISIONS.md` — Architectural decision log (ADRs in `docs/decisions/`)
- `CLAUDE.md` / `AGENTS.md` — AI coding agent rules

## Local development

See `docs/onboarding/SETUP.md` (will be populated in Phase 1).

## License

MIT — see `LICENSE`.
