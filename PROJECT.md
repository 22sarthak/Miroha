# Project context — Miroha

This is the document that orients a new contributor (human or AI agent) in 5 minutes.

## What we're building

Miroha is an AI-powered movie and web-series discovery platform with a personal Curator. Three things differentiate it:

1. **Cross-OTT discovery for India + global**: aggregates availability across Netflix, Prime, JioHotstar, JioCinema, SonyLIV, MUBI, ZEE5, Apple TV+, Disney+, etc.
2. **The Curator**: an AI Miroha companion with persistent memory of the user's taste, conversations, reactions, and history. Configurable personalities (MVP ships only "Buddy"; Snob and Wildcard come in v1.1).
3. **Explainable recommendations**: every "Why this?" references the user's actual history, not generic platitudes.

## Target users

**Primary (MVP)**: Cinephiles in India and globally — people whose taste matters to them, who already use Letterboxd or MUBI, who are frustrated by streaming-platform algorithms.

**Expansion (post-MVP)**: mass-market discovery users who don't yet know what they want to watch, served by the same product as it earns trust through the Miroha cohort.

## Positioning

Hybrid: Cinephiles-first → mass-market. Cinephiles are the wedge audience because they have high willingness to pay and create the trust signal that pulls mass-market in. We are NOT trying to be Netflix-for-everyone on day one.

## Current phase

**Phase 0 — Repo and governance setup.**

Active work: scaffold the monorepo, establish coding conventions, write architectural docs.

After Phase 0, the build proceeds in phases 1–11 (see `ARCHITECTURE.md` and chat history for the roadmap).

## Decisions made (see DECISIONS.md for ADRs)

- **Curator personalities at MVP**: ship Buddy only. Snob + Wildcard architecture exists but is not exposed.
- **Geography**: India + global staged launch. India MVP at week 12, global expansion at week 16.
- **Stack**: free-tier managed services (Cloudflare Pages, Fly.io, Neon, Upstash, Clerk, Inngest). Domain is the only paid item at MVP.
- **LLMs**: Gemini 2.5 Flash primary, Groq for cheap classification, OpenRouter for failover. v1.1 upgrades to Claude Sonnet for the Curator and explanations.
- **Embeddings**: Jina v3 multilingual, 1024-dim.
- **Database**: Neon Postgres + pgvector (NOT Supabase — see ADR-0001).
- **Launch strategy**: public waitlist with rolling invites.

## Out of scope for MVP

- Watch parties (v1.1+)
- Taste twins / social graph (v1.1+)
- Multiple Curator personalities exposed in UI (v1.1+)
- Voice input (v1.1+)
- Full 3D Taste DNA visualization (v1.1+; basic glyph in MVP)
- Mobile native apps (v2+)
- B2B features (v2+)
- User-generated reviews (read-only at MVP)

## Success criteria for MVP

By end of week 12 (India MVP):
- 1000 invited users from waitlist
- 60%+ complete onboarding (the 30-film calibration)
- 30%+ have a Curator conversation in the first session
- 4.0+ avg star rating from beta users on Curator quality
- Affiliate clicks tracked (revenue is a v1 goal, not MVP)

By end of week 16 (global expansion):
- Catalog covers top 80% of titles on major Western OTTs
- Geographic latency under 400ms p95 from India, US, UK, EU
- 5000+ users on the platform

## Communication

- All architectural decisions get an ADR in `docs/decisions/`
- All cross-agent context goes in commit messages and PROJECT.md
- When uncertain, ask the user — don't guess on architecture or product
