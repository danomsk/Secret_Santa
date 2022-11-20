from aiogram.types import InlineKeyboardMarkup, inline_keyboard, InlineKeyboardButton

check = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Давай же узнаем кто это!", callback_data="check")
    ]
])
