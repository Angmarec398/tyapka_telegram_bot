from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.filters.command import CommandObject
from aiogram.types import Message

from app import api_client
from app.api_client import BackendError
from app.texts import LINKED_OK, TOKEN_EXPIRED, TOKEN_USED, WELCOME_NO_TOKEN

router = Router()


@router.message(CommandStart(deep_link=True))
async def cmd_start_with_token(message: Message, command: CommandObject) -> None:
    token = (command.args or "").strip()
    if not token or len(token) > 128:
        await message.answer(TOKEN_EXPIRED)
        return
    chat_id = message.chat.id
    display_name = message.from_user.full_name if message.from_user else None

    try:
        data = await api_client.link(token, chat_id, display_name)
    except BackendError as exc:
        if exc.status_code == 404:
            await message.answer(TOKEN_EXPIRED)
        elif exc.status_code == 409:
            await message.answer(TOKEN_USED)
        else:
            raise
        return

    username = data.get("username") or "пользователь"
    await message.answer(LINKED_OK.format(username=username))


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(WELCOME_NO_TOKEN)
