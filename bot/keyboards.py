from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_town_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Горячий Ключ", callback_data="Горячий Ключ"),
            InlineKeyboardButton(text="Пятигорская", callback_data="Пятигорская")
        ]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    return kb


def sub_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Подписаться", callback_data="subscribe"),
            InlineKeyboardButton(text="Отписаться", callback_data="unsubscribe")
        ],
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    return kb
