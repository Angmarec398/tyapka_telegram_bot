from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app import api_client
from app.api_client import BackendError
from app.texts import (
    STATUS_NOT_LINKED,
    TODAY_DIGEST_EMPTY,
    TODAY_DIGEST_HEADER,
    TODAY_EVENTS_SECTION,
    TODAY_WATERING_SECTION,
)

router = Router()


@router.message(Command("today"))
async def cmd_today(message: Message) -> None:
    try:
        data = await api_client.digest_today(message.chat.id)
    except BackendError as exc:
        if exc.status_code == 404:
            await message.answer(STATUS_NOT_LINKED)
            return
        raise

    if not data.get("has_content"):
        await message.answer(TODAY_DIGEST_EMPTY)
        return

    parts: list[str] = [TODAY_DIGEST_HEADER]

    waterings: list[dict] = data.get("waterings") or []
    if waterings:
        parts.append(TODAY_WATERING_SECTION)
        for w in waterings:
            parts.append(f"  • {w['plant_name']} (грядка: {w['bed_name']})\n")

    events: list[dict] = data.get("events") or []
    if events:
        if waterings:
            parts.append("\n")
        parts.append(TODAY_EVENTS_SECTION)
        for ev in events:
            parts.append(f"  • {ev['title']}\n")

    await message.answer("".join(parts))
