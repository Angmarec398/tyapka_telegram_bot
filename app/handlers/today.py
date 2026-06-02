from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app import api_client
from app.api_client import BackendError
from app.keyboards.nav import TODAY_KEYBOARD
from app.texts import (
    STATUS_NOT_LINKED,
    TODAY_DIGEST_EMPTY,
    TODAY_DIGEST_HEADER,
    TODAY_EVENTS_SECTION,
    TODAY_HARVEST_SECTION,
    TODAY_WATERING_SECTION,
)

router = Router()


def _fmt_ml(ml: int) -> str:
    if ml >= 1000:
        return f"{ml / 1000:g} л"
    return f"{ml} мл"


def _fmt_volume(vol_min: int, vol_max: int) -> str:
    return f"Объём воды: {_fmt_ml(vol_min)} — {_fmt_ml(vol_max)}"


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
        await message.answer(TODAY_DIGEST_EMPTY, reply_markup=TODAY_KEYBOARD)
        return

    parts: list[str] = [TODAY_DIGEST_HEADER]

    waterings: list[dict] = data.get("waterings") or []
    if waterings:
        parts.append(TODAY_WATERING_SECTION)
        for w in waterings:
            vol = _fmt_volume(w.get("vol_min_ml", 0), w.get("vol_max_ml", 0))
            parts.append(f"  • {w['plant_name']} (грядка: {w['bed_name']}): {vol}\n")

    harvests: list[dict] = data.get("harvests") or []
    if harvests:
        if waterings:
            parts.append("\n")
        parts.append(TODAY_HARVEST_SECTION)
        for h in harvests:
            parts.append(f"  • {h['plant_name']} (грядка: {h['bed_name']})\n")

    events: list[dict] = data.get("events") or []
    if events:
        if waterings or harvests:
            parts.append("\n")
        parts.append(TODAY_EVENTS_SECTION)
        for ev in events:
            parts.append(f"  • {ev['title']}\n")

    await message.answer("".join(parts), reply_markup=TODAY_KEYBOARD)
