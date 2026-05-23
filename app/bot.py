import socket

from aiohttp import TCPConnector
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

from app.config import settings
from app.handlers import help, mute, start, status, unlink
from app.middlewares.errors import ErrorMiddleware
from app.middlewares.logging import LoggingMiddleware


def create_bot() -> Bot:
    session = AiohttpSession(connector=TCPConnector(family=socket.AF_INET))
    return Bot(
        token=settings.TELEGRAM_BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )


def create_dispatcher() -> Dispatcher:
    dp = Dispatcher()

    dp.update.outer_middleware(LoggingMiddleware())
    dp.update.outer_middleware(ErrorMiddleware())

    dp.include_router(start.router)
    dp.include_router(status.router)
    dp.include_router(mute.router)
    dp.include_router(unlink.router)
    dp.include_router(help.router)

    return dp
