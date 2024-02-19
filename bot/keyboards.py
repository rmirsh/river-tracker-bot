from typing import List

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def get_town_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Горячий Ключ", callback_data="goryachiy kluch"),
            InlineKeyboardButton(text="Пятигорская", callback_data="pyatigorskaya"),
        ]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    return kb


def sub_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Подписаться", callback_data="subscribe"),
            InlineKeyboardButton(text="Отписаться", callback_data="unsubscribe"),
        ],
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    return kb


def choose_town_kb() -> ReplyKeyboardMarkup:
    """
    Возвращает клавиатуру для двух городов
    :return: объект реплай-клавиатуры
    """
    buttons = [
        [KeyboardButton(text="Горячий Ключ"), KeyboardButton(text="Пятигорская")]
    ]
    kb = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Нажмите на кнопку ниже",
    )

    return kb


def make_row_keyboard(items: list[str] | str) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    if isinstance(items, str):
        items = [items]

    row = [KeyboardButton(text=item) for item in items]
    # TRY one time keyboard
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)
