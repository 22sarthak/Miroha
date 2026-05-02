# Architecture — Miroha

## System overview

Miroha is a Next.js frontend on Cloudflare Pages, talking to a FastAPI backend on Fly.io, backed by Neon Postgres (with pgvector), Upstash Redis, Cloudflare R2, and Clerk for auth. Background jobs run on Inngest. All LLM calls go through a single internal LLM Router that fans out to Gemini, Groq, and OpenRouter today (Claude Sonnet in v1.1).
User browser
↓
Cloudflare Pages (Next.js 14)
↓
FastAPI (Fly.io)
├── Clerk (auth)
├── Neon Postgres (catalog + users + pgvector)
├── Upstash Redis (cache + rate limits)
├── Cloudflare R2 (object storage)
├── Inngest (background jobs)
└── LLM Router
├── Gemini 2.5 Flash    (primary)
├── Groq Llama 3        (cheap classification)
├── OpenRouter DeepSeek (failover)
└── Claude Sonnet       (v1.1 upgrade)
External: TMDB API (catalog source)

## Why this shape

- **Free at MVP scale**: every component has a free tier sufficient for a closed beta of 1000+ users.
- **Geopolitically resilient**: Neon (not Supabase — Supabase was blocked in India Feb 24–March 4, 2026; we won't take that risk on the wedge market).
- **AI layer is fluid, infra is sticky**: model swaps are config changes; database swaps are migrations. Architected to that asymmetry.
- **Single LLM Router**: prevents vendor lock-in to any one model and lets us upgrade Curator quality with a one-line config change.

## Data model

Five conceptual clusters:

1. **Identity**: `users`, `taste_profiles`
2. **Catalog**: `films`, `film_embeddings`, `ott_platforms`, `film_availability`
3. **Interactions**: `interactions` (append-mostly event log)
4. **Curator**: `curator_conversations`, `curator_messages`, `curator_memory_facts`, `taste_evolution_snapshots`
5. **Growth**: `waitlist`

The full DDL is created in Phase 2 via Alembic migrations. See `docs/architecture/data-model.md` for table-by-table commentary (created in Phase 2).

### Key design choices

- **`interactions` is append-mostly**. Corrections are new events with new `interaction_type`. The `taste_profiles.taste_vector` is the materialized view, recomputed by Inngest.
- **Embeddings live in `film_embeddings`, separate from `films`**. This keeps ANN indexing clean and lets us re-embed without touching the catalog table.
- **`curator_memory_facts.superseded_by_id`** handles taste evolution: facts aren't deleted, they're marked superseded. The Curator can still reason about "you used to love X, you've cooled on it."
- **1024-dim embeddings** to support Jina v3 (free tier, multilingual) or Cohere multilingual-v3 (paid upgrade) without dimension migration.

## LLM Router

Every LLM call in the codebase goes through `apps/api/app/llm/router.py`. The router routes by *task type*, not by model name. Tasks include `CURATOR_CHAT`, `EXPLANATION`, `QUERY_PARSE`, `SPOILER_DETECT`, `MOOD_TAG`, `REVIEW_SUMMARIZE`, `MEMORY_EXTRACT`.

For each task, a configured ordered list of `(provider, model)` pairs defines:
- **Primary**: first entry; serves all calls when healthy.
- **Failover**: subsequent entries; activated on timeout, 429, or 5xx.

Concrete config (MVP):

| Task | Primary | Failover |
|------|---------|----------|
| CURATOR_CHAT | Gemini 2.5 Flash | OpenRouter DeepSeek |
| EXPLANATION | Gemini 2.5 Flash | OpenRouter DeepSeek |
| QUERY_PARSE | Gemini 2.5 Flash | Groq Llama 3.3 70B |
| SPOILER_DETECT | Groq Llama 3.1 8B | Gemini 2.5 Flash |
| MOOD_TAG | Groq Llama 3.1 8B | Gemini 2.5 Flash |
| REVIEW_SUMMARIZE | Gemini 2.5 Flash | Groq Llama 3.3 70B |
| MEMORY_EXTRACT | Gemini 2.5 Flash | Groq Llama 3.3 70B |

The router also handles caching (Upstash-backed, keyed by task + content hash) and telemetry (every call emits a PostHog event).

## Curator memory architecture

Three memory layers compose into every Curator turn:

1. **Session context** — recent messages in the active conversation (last ~20 turns)
2. **Profile** — structured user state: taste vector, OTT subscriptions, recent interactions, Curator preferences
3. **Facts** — extracted long-term memory facts (`curator_memory_facts`), retrieved via embedding similarity to the current user message

Detailed in `docs/curator/memory-architecture.md` (created in Phase 7).

## Recommendation pipeline

For a given user query/context:

1. **Cold start check**: if user has fewer than 30 interactions, weight the calibration vector heavily; otherwise rely on the live taste vector.
2. **Candidate retrieval**: pgvector ANN search over `film_embeddings`, filtered by region OTT availability, returning top 200 candidates.
3. **Reranking**: blend ANN score with diversity penalty, recency, popularity prior, and (for personalized requests) similarity to recent loved films.
4. **LLM rerank** of top 30 with structured output: final ordering plus per-film "Why this?" generation.
5. **Cache** results in `recommendations` with 24h TTL.

Detailed in `docs/architecture/recommendation-pipeline.md` (created in Phase 8).

## Onboarding (cold start)

10–12 minute flow:

1. Brief intro to the Curator concept, Buddy personality default
2. 30-film calibration sprint — films sampled to span the embedding space (era, country, register, pacing). User marks each Loved/Liked/Meh/Hated/Haven't seen.
3. Free-text taste statement (embedded and added to taste vector)
4. OTT subscription toggles
5. First Curator conversation — Curator opens with 3 recommendations, asks for live reactions

Detailed in `docs/onboarding/cold-start.md` (created in Phase 6).

## Deployment

- **Frontend**: Cloudflare Pages, deployed on push to main via Git integration
- **Backend**: Fly.io, `fly deploy` from CI
- **Database migrations**: Alembic, run on backend startup with idempotency lock
- **Background jobs**: Inngest, deploy via Inngest dashboard or Git integration

## Observability

- **Errors**: Sentry (5k errors/month free)
- **Product analytics**: PostHog (1M events/month free)
- **Logs**: Axiom or Better Stack (free tiers)
- **LLM telemetry**: every call emits `llm_call` event with provider/model/tokens/latency to PostHog

## Cost ceiling at MVP

Target: $0/month for compute, ~$12/year for the domain.

Realistic burn during the first 1000 users: $0–15/month total. Free tiers cover everything except the domain.

Upgrade ladder (in priority order if/when free tiers are exceeded):
1. Domain (~$12/year) — already paid
2. Claude Sonnet for Curator chat (~$30/month)
3. Vercel Pro if Cloudflare Pages becomes painful (~$20/month)
4. Neon Pro if 0.5GB or compute limits hit (~$19/month)
