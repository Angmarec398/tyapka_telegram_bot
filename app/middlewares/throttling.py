"""Middleware для защиты от спама: ограничивает частоту запросов на пользователя."""

import time
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject, Update

_RATE_LIMIT = 1.0  # минимальный интервал между запросами одного пользователя, секунды
_THROTTLE_TEXT = "⏳ Не так быстро. Подождите секунду."

_last_seen: dict[int, float] = {}


class ThrottlingMiddleware(BaseMiddleware):
    """Пропускает не более одного запроса в секунду на пользователя.

    Игнорирует обновления без user_id (например, анонимные сообщения в канала��).
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user_id = _extract_user_id(event)
        if user_id is not None:
            now = time.monotonic()
            last = _last_seen.get(user_id, 0.0)
            if now - last < _RATE_LIMIT:
                if isinstance(event, Update) and event.message:
                    await event.message.answer(_THROTTLE_TEXT)
                return None
            _last_seen[user_id] = now
        return await handler(event, data)


def _extract_user_id(event: TelegramObject) -> int | None:
    """Извлечь user_id из Update, если возможно."""
    if not isinstance(event, Update):
        return None
    if event.message and event.message.from_user:
        return event.message.from_user.id
    if event.callback_query and event.callback_query.from_user:
        return event.callback_query.from_user.id
    return None
