"""Middleware для логирования входящих обновлений."""

import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    """Логирует каждое входящее обновление: update_id, user_id, chat_id, команда или callback."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if isinstance(event, Update):
            update = event
            user_id = chat_id = command = None

            if update.message:
                msg = update.message
                user_id = msg.from_user.id if msg.from_user else None
                chat_id = msg.chat.id
                command = msg.text.split()[0] if msg.text and msg.text.startswith("/") else "<message>"
            elif update.callback_query:
                cb = update.callback_query
                user_id = cb.from_user.id if cb.from_user else None
                chat_id = cb.message.chat.id if cb.message else None
                command = f"<callback:{cb.data}>"

            logger.info(
                "update=%d user=%s chat=%s cmd=%s",
                update.update_id, user_id, chat_id, command,
            )

        return await handler(event, data)
