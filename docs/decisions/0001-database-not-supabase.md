# ADR-0001: Database — Neon, not Supabase

- **Status**: Accepted
- **Date**: 2026-05-01
- **Deciders**: Sarthak

## Context

We need a managed Postgres provider with pgvector support, ideally on a free tier, for an India + global launch. Supabase was the obvious first choice — generous free tier, native pgvector, branching, integrated auth, used by 365k+ Indian developers in January 2026 alone.

However, on February 24, 2026, the Indian government issued a Section 69A blocking order against Supabase, taking it offline for Indian users for 8 days. Access was restored on March 4, 2026, but the precedent is set: a single ISP-level block can take down our database connectivity for the wedge market with zero notice and no public reasoning. The original block reason was never disclosed.

For a product whose entire MVP positioning leans on India as the wedge market, accepting that single point of failure is unacceptable.

## Decision

Use **Neon** as the managed Postgres provider. Use **Clerk** for auth (separating concerns from the database, also avoiding any single-vendor "blast radius"). Use **Upstash** for Redis.

Code architecture is vendor-abstracted: SQLAlchemy ORM, repository pattern, no Neon-specific features in business logic. If we ever need to migrate (to AWS Mumbai RDS as the bulletproof fallback), it's a 2-week sprint, not a rewrite.

## Consequences

### Positive
- No single-vendor concentration risk for India
- Neon's branching feature is genuinely useful for preview environments
- Free tier (0.5 GB storage + 191 compute hours) is sufficient for closed beta
- Migration path to AWS Mumbai is clean given the abstraction layer

### Negative
- Have to integrate Clerk separately rather than use Supabase Auth
- Slightly more configuration overhead (3 services instead of 1)
- Lose Supabase realtime subscriptions (we don't need them at MVP)

### Trade-offs accepted
- Vendor lock-in to Neon for now, mitigated by ORM abstraction

## Alternatives considered

- **Supabase**: rejected due to demonstrated geopolitical risk for India market.
- **AWS Mumbai RDS + ECS**: bulletproof on geography, but slows MVP velocity by 2–3 weeks. Held as the fallback if Neon ever has problems.
- **PlanetScale**: rejected — MySQL, no pgvector.
- **Render Postgres**: rejected — fewer regions, less mature pgvector support.
