"""Обработчики навигационных Inline-кнопок (callback_data вида nav:*)."""

from aiogram import F, Router
from aiogram.types import CallbackQuery

from app import api_client
from app.api_client import BackendError
from app.keyboards.mute import MUTE_KEYBOARD
from app.keyboards.nav import (
    AFTER_MUTE_KEYBOARD,
    AFTER_UNMUTE_KEYBOARD,
    STATUS_KEYBOARD,
    TODAY_KEYBOARD,
)
from app.texts import (
    FREQUENCY_LABELS,
    MUTE_CHOOSE,
    MUTE_DURATION_LABELS,
    MUTED_LINE,
    MUTED_UNTIL,
    STATUS_LINKED,
    STATUS_NOT_LINKED,
    TODAY_DIGEST_EMPTY,
    TODAY_DIGEST_HEADER,
    TODAY_EVENTS_SECTION,
    TODAY_HARVEST_SECTION,
    TODAY_WATERING_SECTION,
    UNLINK_CONFIRM,
    UNMUTED,
)
from app.handlers.unlink import _CONFIRM_KEYBOARD

router = Router()


def _yn(val: bool) -> str:
    return "✅" if val else "❌"


def _fmt_ml(ml: int) -> str:
    if ml >= 1000:
        return f"{ml / 1000:g} л"
    return f"{ml} мл"


def _fmt_volume(vol_min: int, vol_max: int) -> str:
    return f"Объём воды: {_fmt_ml(vol_min)} — {_fmt_ml(vol_max)}"


@router.callback_query(F.data == "nav:status")
async def cb_nav_status(callback: CallbackQuery) -> None:
    data = await api_client.status(callback.message.chat.id)

    if not data.get("linked"):
        await callback.message.edit_text(STATUS_NOT_LINKED)
        await callback.answer()
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

    notifications_enabled = user.get("notifications_enabled", True)
    enabled_label = "✅ Включены" if notifications_enabled else "❌ Выключены"

    text = STATUS_LINKED.format(
        username=user.get("username") or "—",
        notifications_enabled=enabled_label,
        timezone=data.get("timezone") or user.get("timezone") or "—",
        window_start=window.get("start") or user.get("notify_window_start") or "—",
        window_end=window.get("end") or user.get("notify_window_end") or "—",
        frequency=frequency,
        watering=_yn(flags.get("watering", user.get("notify_watering", False))),
        harvest=_yn(flags.get("harvest", user.get("notify_harvest", False))),
        calendar=_yn(flags.get("calendar", user.get("notify_calendar", False))),
        mute_line=mute_line,
    )
    await callback.message.edit_text(text, reply_markup=STATUS_KEYBOARD)
    await callback.answer()


@router.callback_query(F.data == "nav:today")
async def cb_nav_today(callback: CallbackQuery) -> None:
    try:
        data = await api_client.digest_today(callback.message.chat.id)
    except BackendError as exc:
        if exc.status_code == 404:
            await callback.message.edit_text(STATUS_NOT_LINKED)
            await callback.answer()
            return
        raise

    if not data.get("has_content"):
        await callback.message.edit_text(TODAY_DIGEST_EMPTY, reply_markup=TODAY_KEYBOARD)
        await callback.answer()
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

    await callback.message.edit_text("".join(parts), reply_markup=TODAY_KEYBOARD)
    await callback.answer()


@router.callback_query(F.data == "nav:mute")
async def cb_nav_mute(callback: CallbackQuery) -> None:
    await callback.message.edit_text(MUTE_CHOOSE, reply_markup=MUTE_KEYBOARD)
    await callback.answer()


@router.callback_query(F.data == "nav:unmute")
async def cb_nav_unmute(callback: CallbackQuery) -> None:
    await api_client.unmute(callback.message.chat.id)
    await callback.message.edit_text(UNMUTED, reply_markup=AFTER_UNMUTE_KEYBOARD)
    await callback.answer()


@router.callback_query(F.data == "nav:unlink")
async def cb_nav_unlink(callback: CallbackQuery) -> None:
    await callback.message.edit_text(UNLINK_CONFIRM, reply_markup=_CONFIRM_KEYBOARD)
    await callback.answer()
