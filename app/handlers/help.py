from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.texts import FALLBACK, HELP

router = Router()


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(HELP)


@router.message()
async def fallback(message: Message) -> None:
    await message.answer(FALLBACK)
