# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Security

**STRICT RULE: Never read, display, analyze, or reference the contents of `.env`.**
- This file contains real credentials: bot token, internal API token, backend URL, and other secrets.
- Do NOT open it, cat it, grep it, or include any part of it in responses.
- If a task requires knowing configuration values, ask the user directly.

## Git workflow

**STRICT RULE: Always work directly on the `master` branch.**
- NEVER create feature branches.
- NEVER use worktrees (`EnterWorktree`, `/worktree`, or any equivalent).
- NEVER use plan mode that auto-creates worktrees — decline or exit immediately.
- All edits, commits, and commands must happen in the main working directory on `master`.

## Code style

All Python code must follow these standards:

- **PEP 8** — formatting and naming: `snake_case` for functions/variables, `UPPER_CASE` for module-level constants, max line length 88 characters, imports ordered (stdlib → third-party → local).
- **PEP 257** — docstrings: module-level docstring in every file, class docstring for every class, one-line docstring for public functions where the purpose is non-obvious. Blank line after class docstring before first method.
- **PEP 585** — built-in generics: use `dict[str, Any]`, `list[int]`, `X | None` instead of `Dict`, `List`, `Optional` from `typing`.

## Commands

```bash
# Run bot (from project root with .venv active)
.venv/Scripts/python.exe -m app.main       # run bot directly
docker compose up --build                   # build and run via Docker
docker compose up -d                        # detached

# Dependencies
.venv/Scripts/pip.exe install -r requirements.txt
```

## Architecture

**Stack:** Python 3.12, aiogram 3.x, httpx, pydantic-settings.

**Entry point:** `app/` — aiogram long-polling bot. Config loaded via pydantic-settings from `.env` (with `extra="ignore"` — .env may contain extra backend-only fields).

**No direct DB access** — all data operations go through the backend internal API (`/internal/telegram/*`) using `X-Internal-Token` header auth.

**Key env vars:** `TELEGRAM_BOT_TOKEN`, `INTERNAL_API_TOKEN`, `BACKEND_BASE_URL`.

**Deployment:** standalone `docker-compose.yml` with WireGuard VPN container for backend connectivity.

## Key architectural decisions

- **Long-polling only** — webhook mode is not implemented and `TELEGRAM_USE_WEBHOOK` has been removed.
- **Centralized error handling** — all exceptions are caught in `ErrorMiddleware`; handlers raise freely.
- **Throttling** — `ThrottlingMiddleware` limits to 1 request/second per user (in-memory).
- **Single source of truth for texts** — all user-facing strings and labels live in `app/texts.py`.
- **Inline navigation** — `app/keyboards/nav.py` defines navigation keyboards; `app/handlers/nav.py` handles all `nav:*` callbacks, reusing the same display logic as the command handlers. `/help` is the only command without Inline-buttons.
- **Secrets** — `BACKEND_BASE_URL` and all credentials are stored in GitHub Secrets, never hardcoded in CI/CD.

## Last reviewed commit

`7dbbc7a` — Корректировка кнопок (2026-06-02)
