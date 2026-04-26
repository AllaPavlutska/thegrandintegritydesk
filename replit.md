# Workspace

## Overview

pnpm workspace monorepo using TypeScript. Each package manages its own dependencies.

## Stack

- **Monorepo tool**: pnpm workspaces
- **Node.js version**: 24
- **Package manager**: pnpm
- **TypeScript version**: 5.9
- **API framework**: Express 5
- **Database**: PostgreSQL + Drizzle ORM
- **Validation**: Zod (`zod/v4`), `drizzle-zod`
- **API codegen**: Orval (from OpenAPI spec)
- **Build**: esbuild (CJS bundle)
- **Python app**: Streamlit "Grand Integrity Desk" URL analyzer served on port 5000

## Python project layout

- `app.py` — thin Streamlit entry point; composes the UI and delegates work
- `analyzer/` — analysis package (no Streamlit imports inside the engine):
  - `constants.py` — satire / restricted / state-media blacklists, trigger lexicon
  - `validators.py` — `is_local_url` URL guards
  - `database.py` — `DatabaseManager` SQLite wrapper (`safety_pipeline.db`)
  - `engine.py` — `MisinformationEngine`, `DomainStatus`, `AnalysisResult`; supports
    a pluggable `fetcher` for tests so no network is required
  - `ui.py` — Streamlit CSS injection and copy strings
- `tests/` — pytest suite (`test_validators.py`, `test_database.py`, `test_engine.py`)

## Key Commands

- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- `pnpm --filter @workspace/api-server run dev` — run API server locally
- `streamlit run app.py --server.port 5000` — run the Streamlit analyzer app
- `python -m pytest` — run the analyzer test suite

See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details.
