from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

mute_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1 час", callback_data="mute:1h"),
            InlineKeyboardButton(text="До завтра", callback_data="mute:until_tomorrow"),
            InlineKeyboardButton(text="На неделю", callback_data="mute:1w"),
        ]
    ]
)
