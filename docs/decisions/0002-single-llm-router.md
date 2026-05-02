# ADR-0002: Single LLM Router for all model calls

- **Status**: Accepted
- **Date**: 2026-05-01
- **Deciders**: Sarthak

## Context

We use multiple LLM providers (Gemini, Groq, OpenRouter at MVP; Claude Sonnet in v1.1) for different task types and as failover for each other. Without an abstraction, every feature would import LLM SDKs directly, hardcode model names, and reimplement caching/retry logic.

We also need to swap models without rewriting features — the v1.1 upgrade from Gemini Flash to Claude Sonnet for Curator chat needs to be a config change, not a refactor.

## Decision

All LLM calls go through `apps/api/app/llm/router.py`. The router:

- Routes by **task type** (CURATOR_CHAT, EXPLANATION, etc.), not model name
- Maintains an ordered list of `(provider, model)` pairs per task: primary first, failovers next
- Handles caching (Upstash-backed, keyed by task + content hash)
- Handles failover on timeout, 429, 5xx
- Emits telemetry on every call (provider, model, tokens, latency)

No code outside `apps/api/app/llm/providers/` imports an LLM SDK. This is enforced as a coding convention in CLAUDE.md / AGENTS.md.

## Consequences

### Positive
- Model upgrade in v1.1 = one-line config change
- Cost optimization is centralized (cache hits, cheap-task routing to Groq)
- Telemetry tells us which tasks/providers are expensive or flaky
- Easier to test (mock the router, not 5 different SDKs)

### Negative
- Adds a layer; for very simple use cases this feels like over-engineering
- Provider-specific features (e.g. Gemini's native image input) require thoughtful abstraction

### Trade-offs accepted
- We won't use bleeding-edge provider-specific features unless they're worth abstracting

## Alternatives considered

- **Per-feature LLM clients**: rejected — drift, no central caching, painful to upgrade.
- **LangChain or LlamaIndex**: rejected — too heavy for our needs, opinions we'd have to fight.
