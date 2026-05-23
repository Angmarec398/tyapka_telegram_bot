import logging
from typing import Any

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

_client: httpx.AsyncClient | None = None


class BackendError(Exception):
    def __init__(self, status_code: int, detail: str = "") -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"Backend {status_code}: {detail}")


def get_client() -> httpx.AsyncClient:
    if _client is None:
        raise RuntimeError("API client not initialized")
    return _client


async def init_client() -> None:
    global _client
    _client = httpx.AsyncClient(
        base_url=settings.BACKEND_BASE_URL,
        headers={"X-Internal-Token": settings.INTERNAL_API_TOKEN},
        timeout=5.0,
    )


async def close_client() -> None:
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None


async def _request(method: str, url: str, **kwargs: Any) -> Any:
    client = get_client()
    last_exc: Exception | None = None
    for attempt in range(2):
        try:
            resp = await client.request(method, url, **kwargs)
            if resp.status_code >= 400:
                try:
                    detail = resp.json().get("detail", "")
                except Exception:
                    detail = resp.text
                if attempt == 0 and resp.status_code >= 500:
                    last_exc = BackendError(resp.status_code, detail)
                    continue
                raise BackendError(resp.status_code, detail)
            return resp.json()
        except (httpx.ConnectError, httpx.TimeoutException) as exc:
            logger.error("Backend network error (attempt %d): %s", attempt + 1, exc)
            last_exc = exc
    raise last_exc  # type: ignore[misc]


async def link(token: str, chat_id: int, display_name: str | None) -> dict:
    return await _request(
        "POST",
        "/internal/telegram/link",
        json={"token": token, "chat_id": chat_id, "display_name": display_name},
    )


async def status(chat_id: int) -> dict:
    return await _request("GET", "/internal/telegram/status", params={"chat_id": chat_id})


async def mute(chat_id: int, duration: str) -> dict:
    return await _request(
        "POST",
        "/internal/telegram/mute",
        json={"chat_id": chat_id, "duration": duration},
    )


async def unmute(chat_id: int) -> dict:
    return await _request("POST", "/internal/telegram/unmute", json={"chat_id": chat_id})


async def unlink(chat_id: int) -> dict:
    return await _request("DELETE", "/internal/telegram/channel", params={"chat_id": chat_id})
