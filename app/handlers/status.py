from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app import api_client
from app.texts import (
    FREQUENCY_LABELS,
    MUTED_LINE,
    STATUS_LINKED,
    STATUS_NOT_LINKED,
)

router = Router()


def _yn(val: bool) -> str:
    return "✅" if val else "❌"


@router.message(Command("status"))
async def cmd_status(message: Message) -> None:
    data = await api_client.status(message.chat.id)

    if not data.get("linked"):
        await message.answer(STATUS_NOT_LINKED)
        return

    user = data.get("user") or {}
    window = data.get("window") or {}
    flags = data.get("flags") or {}
    muted_until = data.get("muted_until")

    frequency_raw = user.get("notify_frequency", "daily")
    frequency = FREQUENCY_LABELS.get(frequency_raw, frequency_raw)

    mute_line = ""
    if muted_until:
        mute_line = MUTED_LINE.format(until=muted_until[:16].replace("T", " "))

    text = STATUS_LINKED.format(
        username=user.get("username") or "—",
        timezone=data.get("timezone") or user.get("timezone") or "—",
        window_start=window.get("start") or user.get("notify_window_start") or "—",
        window_end=window.get("end") or user.get("notify_window_end") or "—",
        frequency=frequency,
        watering=_yn(flags.get("watering", user.get("notify_watering", False))),
        calendar=_yn(flags.get("calendar", user.get("notify_calendar", False))),
        notes=_yn(flags.get("notes", user.get("notify_notes", False))),
        mute_line=mute_line,
    )
    await message.answer(text)
