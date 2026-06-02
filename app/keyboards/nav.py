"""Навигационные Inline-клавиатуры для основных команд бота."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

_BTN_STATUS = InlineKeyboardButton(text="📋 Статус", callback_data="nav:status")
_BTN_TODAY = InlineKeyboardButton(text="🌱 Список дел", callback_data="nav:today")
_BTN_MUTE = InlineKeyboardButton(text="🔕 Приостановить", callback_data="nav:mute")
_BTN_UNMUTE = InlineKeyboardButton(text="🔔 Возобновить", callback_data="nav:unmute")
_BTN_UNLINK = InlineKeyboardButton(text="🔓 Отвязать", callback_data="nav:unlink")

# После успешной привязки (/start с токеном)
AFTER_LINK_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[[_BTN_STATUS, _BTN_TODAY]]
)

# После /status
STATUS_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [_BTN_TODAY],
        [_BTN_MUTE],
        [_BTN_UNLINK],
    ]
)

# После /today
TODAY_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[[_BTN_STATUS]]
)

# После /unmute
AFTER_UNMUTE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[[_BTN_STATUS, _BTN_TODAY]]
)

# После выбора длительности /mute
AFTER_MUTE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[[_BTN_STATUS, _BTN_UNMUTE]]
)
