from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app import api_client
from app.keyboards.mute import mute_keyboard
from app.texts import MUTE_CHOOSE, MUTED_UNTIL, UNMUTED

router = Router()

_DURATION_LABELS = {
    "mute:1h": "1 час",
    "mute:until_tomorrow": "до завтра",
    "mute:1w": "на неделю",
}


@router.message(Command("mute"))
async def cmd_mute(message: Message) -> None:
    await message.answer(MUTE_CHOOSE, reply_markup=mute_keyboard)


@router.callback_query(F.data.startswith("mute:"))
async def cb_mute(callback: CallbackQuery) -> None:
    duration = callback.data.split(":", 1)[1]
    data = await api_client.mute(callback.message.chat.id, duration)

    muted_until = data.get("muted_until", "")
    if muted_until:
        until_str = muted_until[:16].replace("T", " ")
    else:
        label = _DURATION_LABELS.get(callback.data, duration)
        until_str = label

    await callback.message.edit_text(MUTED_UNTIL.format(until=until_str))
    await callback.answer()


@router.message(Command("unmute"))
async def cmd_unmute(message: Message) -> None:
    await api_client.unmute(message.chat.id)
    await message.answer(UNMUTED)
