# Architectural Decisions — Index

Index of Architectural Decision Records. Each ADR captures a non-trivial architectural choice with its context, the decision, and the consequences. Append a new entry here whenever you create a new ADR.

| # | Title | Status | Date |
|---|-------|--------|------|
| [0001](docs/decisions/0001-database-not-supabase.md) | Database: Neon, not Supabase | Accepted | 2026-05-01 |
| [0002](docs/decisions/0002-single-llm-router.md) | Single LLM Router for all model calls | Accepted | 2026-05-01 |
| [0003](docs/decisions/0003-curator-personalities-staged.md) | Ship Buddy-only at MVP, multi-personality in v1.1 | Accepted | 2026-05-01 |
| [0004](docs/decisions/0004-1024-dim-embeddings.md) | 1024-dimension embeddings (Jina v3 default) | Accepted | 2026-05-01 |

## How to add an ADR

1. Copy `docs/decisions/template.md` to `docs/decisions/NNNN-short-title.md` (next sequential number)
2. Fill it in
3. Add a row to the table above
4. Commit: `git commit -m "docs: ADR-NNNN <title>"`
