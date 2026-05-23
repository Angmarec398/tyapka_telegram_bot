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

## Commands

```bash
# Run bot (from project root with .venv active)
.venv/Scripts/python.exe -m bot            # run bot directly
docker compose up --build                   # build and run via Docker
docker compose up -d                        # detached

# Dependencies
.venv/Scripts/pip.exe install -r requirements.txt
```

## Architecture

**Stack:** Python 3.12, aiogram 3.x, httpx, pydantic-settings.

**Entry point:** `bot/` — aiogram long-polling bot. Config loaded via pydantic-settings from `.env` (with `extra="ignore"` — .env may contain extra backend-only fields).

**No direct DB access** — all data operations go through the backend internal API (`/internal/telegram/*`) using `X-Internal-Token` header auth.

**Key env vars:** `TELEGRAM_BOT_TOKEN`, `INTERNAL_API_TOKEN`, `BACKEND_BASE_URL`.

**Deployment:** standalone `docker-compose.yml` in the bot directory.
