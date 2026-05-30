"""Middleware для централизованной обработки исключений."""

import logging
from typing import Any, Awaitable, Callable

import httpx
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from app.api_client import BackendError
from app.texts import ERR_NOT_LINKED, ERR_UNAVAILABLE, ERR_UNKNOWN

logger = logging.getLogger(__name__)


async def _reply(event: TelegramObject, text: str) -> None:
    if isinstance(event, Message):
        await event.answer(text)
    elif isinstance(event, CallbackQuery):
        await event.answer(text, show_alert=True)


class ErrorMiddleware(BaseMiddleware):
    """Перехватывает сетевые ошибки и BackendError, отправляет пользователю понятное сообщение."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        except (httpx.ConnectError, httpx.TimeoutException) as exc:
            logger.error("Backend unavailable: %s", exc)
            await _reply(event, ERR_UNAVAILABLE)
        except BackendError as exc:
            if exc.status_code == 401:
                logger.critical("INTERNAL_API_TOKEN mismatch — backend returned 401")
                await _reply(event, ERR_UNKNOWN)
            elif exc.status_code == 403:
                await _reply(event, ERR_NOT_LINKED)
            else:
                logger.error("Unhandled BackendError %s: %s", exc.status_code, exc.detail)
                await _reply(event, ERR_UNKNOWN)
        except Exception as exc:
            logger.exception("Unexpected error: %s", exc)
            await _reply(event, ERR_UNKNOWN)
