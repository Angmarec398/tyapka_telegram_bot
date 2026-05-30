from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.texts import MUTE_DURATION_LABELS

mute_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=MUTE_DURATION_LABELS["1h"], callback_data="mute:1h"),
            InlineKeyboardButton(text=MUTE_DURATION_LABELS["until_tomorrow"], callback_data="mute:until_tomorrow"),
            InlineKeyboardButton(text=MUTE_DURATION_LABELS["1w"], callback_data="mute:1w"),
        ]
    ]
)
