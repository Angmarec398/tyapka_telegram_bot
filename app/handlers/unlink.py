from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from app import api_client
from app.texts import UNLINK_CANCEL, UNLINK_CONFIRM, UNLINKED

router = Router()

_CONFIRM_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да, отвязать", callback_data="unlink:yes"),
            InlineKeyboardButton(text="Отмена", callback_data="unlink:no"),
        ]
    ]
)


@router.message(Command("unlink"))
async def cmd_unlink(message: Message) -> None:
    await message.answer(UNLINK_CONFIRM, reply_markup=_CONFIRM_KEYBOARD)


@router.callback_query(F.data == "unlink:yes")
async def cb_unlink_yes(callback: CallbackQuery) -> None:
    await api_client.unlink(callback.message.chat.id)
    await callback.message.edit_text(UNLINKED)
    await callback.answer()


@router.callback_query(F.data == "unlink:no")
async def cb_unlink_no(callback: CallbackQuery) -> None:
    await callback.message.edit_text(UNLINK_CANCEL)
    await callback.answer()
