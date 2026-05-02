# ADR-0004: 1024-dimension embeddings, Jina v3 default

- **Status**: Accepted
- **Date**: 2026-05-01
- **Deciders**: Sarthak

## Context

We need an embedding model for: film catalog embeddings, user taste statements, Curator memory facts, and recommendation similarity search. The model must:

- Be multilingual (Tamil, Telugu, Malayalam, Hindi, Bengali, English at minimum)
- Have a free tier sufficient for MVP scale (~15k catalog embeddings + ongoing user memory facts)
- Have a stable dimension count we can commit to (mid-flight migration is brutal)

## Decision

**Jina embeddings v3** (1024-dim, multilingual, free tier).

Database column: `VECTOR(1024)` everywhere embeddings are stored (`film_embeddings.embedding`, `taste_profiles.taste_vector`, `taste_profiles.statement_embedding`, `curator_memory_facts.fact_embedding`).

Upgrade path within 1024-dim: Cohere embed-multilingual-v3 (paid, slightly higher quality, same dim).

## Consequences

### Positive
- Free at MVP scale
- Multilingual covers our wedge market
- 1024-dim is dense enough for taste-graph fidelity, sparse enough to be cheap
- Upgrade to Cohere is dimension-compatible — no re-embedding required if we just want quality

### Negative
- If we ever want to use OpenAI text-embedding-3-large (3072-dim) or text-embedding-3-small (1536-dim), we re-embed everything

### Trade-offs accepted
- Locked to 1024-dim. Migration off this is an explicit, costly project.

## Alternatives considered

- **Gemini text-embedding-004 (768-dim)**: rejected — lower fidelity, only mild cost saving, breaks compatibility with Cohere upgrade.
- **OpenAI text-embedding-3-small (1536-dim)**: rejected — paid only, no free tier sufficient for our scale.
- **Cohere embed-multilingual-v3 (1024-dim, paid)**: held as the v1+ upgrade target.
