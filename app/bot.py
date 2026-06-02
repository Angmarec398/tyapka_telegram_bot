"""Фабрики для создания экземпляров Bot и Dispatcher с зарегистрированными роутерами и middleware."""

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config import settings
from app.handlers import help, mute, nav, start, status, today, unlink
from app.middlewares.errors import ErrorMiddleware
from app.middlewares.logging import LoggingMiddleware
from app.middlewares.throttling import ThrottlingMiddleware


def create_bot() -> Bot:
    return Bot(
        token=settings.TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )


def create_dispatcher() -> Dispatcher:
    dp = Dispatcher()

    dp.update.outer_middleware(LoggingMiddleware())
    dp.update.outer_middleware(ThrottlingMiddleware())
    dp.update.outer_middleware(ErrorMiddleware())

    dp.include_router(start.router)
    dp.include_router(status.router)
    dp.include_router(today.router)
    dp.include_router(mute.router)
    dp.include_router(unlink.router)
    dp.include_router(nav.router)
    dp.include_router(help.router)

    return dp
