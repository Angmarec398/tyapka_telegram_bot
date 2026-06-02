from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app import api_client
from app.keyboards.mute import MUTE_KEYBOARD
from app.keyboards.nav import AFTER_MUTE_KEYBOARD, AFTER_UNMUTE_KEYBOARD
from app.texts import MUTE_CHOOSE, MUTE_DURATION_LABELS, MUTED_UNTIL, UNMUTED

router = Router()

_VALID_DURATIONS = {"1h", "until_tomorrow", "1w"}


@router.message(Command("mute"))
async def cmd_mute(message: Message) -> None:
    await message.answer(MUTE_CHOOSE, reply_markup=MUTE_KEYBOARD)


@router.callback_query(F.data.startswith("mute:"))
async def cb_mute(callback: CallbackQuery) -> None:
    duration = callback.data.split(":", 1)[1]
    if duration not in _VALID_DURATIONS:
        await callback.answer("Неверное значение", show_alert=True)
        return
    data = await api_client.mute(callback.message.chat.id, duration)

    muted_until = data.get("muted_until", "")
    if muted_until:
        until_str = muted_until[:16].replace("T", " ")
    else:
        until_str = MUTE_DURATION_LABELS.get(duration, duration)

    await callback.message.edit_text(MUTED_UNTIL.format(until=until_str), reply_markup=AFTER_MUTE_KEYBOARD)
    await callback.answer()


@router.message(Command("unmute"))
async def cmd_unmute(message: Message) -> None:
    await api_client.unmute(message.chat.id)
    await message.answer(UNMUTED, reply_markup=AFTER_UNMUTE_KEYBOARD)
