import asyncio
import logging

from app import api_client
from app.bot import create_bot, create_dispatcher
from app.config import settings


async def main() -> None:
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    await api_client.init_client()
    bot = create_bot()
    dp = create_dispatcher()

    me = await bot.get_me()
    logging.getLogger(__name__).info("Bot @%s started, mode=polling", me.username)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await api_client.close_client()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
