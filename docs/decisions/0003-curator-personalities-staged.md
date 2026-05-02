# ADR-0003: Ship Buddy-only at MVP, multi-personality in v1.1

- **Status**: Accepted
- **Date**: 2026-05-01
- **Deciders**: Sarthak

## Context

The Curator concept includes multiple personalities (Buddy, Snob, Wildcard, Scholar) that users can choose between. Shipping all of them at MVP would split prompt-engineering effort, eval coverage, and personality-coherence work three or four ways.

The Curator IS the product — its quality determines whether users believe "this AI gets me." A single exceptional personality beats three mediocre ones for first-impression conversion.

## Decision

MVP ships only **Buddy** (warm, broad appeal). The architecture supports multiple personalities from day one:

- `personality_id` field in `curator_conversations` and `curator_messages`
- Personality-specific system prompts in `packages/prompts/personalities/`
- Personality voice eval suite in `eval/personalities/`

But only Buddy is exposed in the UI. Snob and Wildcard ship as a v1.1 marketing event ("Meet your alternate Curators") with full eval coverage in place.

## Consequences

### Positive
- MVP ships with one excellent voice instead of three mid voices
- v1.1 retention hook is built in
- Architectural support for multi-personality is in place from day one

### Negative
- We don't get the "personalities" differentiation in MVP marketing

### Trade-offs accepted
- Buddy must carry the entire Curator value prop in MVP. We invest disproportionately in Buddy's prompt engineering and eval coverage.

## Alternatives considered

- **Ship all three at MVP**: rejected — quality risk too high.
- **Ship two (Buddy + Snob)**: rejected — Snob is the hardest to nail (Snob done badly is just an asshole), and we don't want to risk it in the first impression.
- **Defer multi-personality architecture entirely**: rejected — retrofitting later is expensive.
