from typing import List

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def get_town_kb() -> InlineKeyboardMarkup:
    """Return an InlineKeyboardMarkup object with buttons for towns.

    This function creates an InlineKeyboardMarkup object with buttons for
    two towns - "Горячий Ключ" and "Пятигорская".

    Returns:
        InlineKeyboardMarkup: An InlineKeyboardMarkup object with town buttons.
    """

    buttons = [
        [
            InlineKeyboardButton(text="Горячий Ключ", callback_data="Горячий Ключ"),
            InlineKeyboardButton(text="Пятигорская", callback_data="Пятигорская"),
        ]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    return kb


def sub_kb() -> InlineKeyboardMarkup:
    """Generate an inline keyboard with subscription options.

    This function creates an inline keyboard with two buttons: "Подписаться"
    for subscribing and "Отписаться" for unsubscribing.

    Returns:
        InlineKeyboardMarkup: An inline keyboard with subscription options.
    """

    buttons = [
        [
            InlineKeyboardButton(text="Подписаться", callback_data="subscribe"),
            InlineKeyboardButton(text="Отписаться", callback_data="unsubscribe"),
        ],
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    return kb


def choose_town_kb() -> ReplyKeyboardMarkup:
    """    Возвращает клавиатуру для выбора между двумя городами.

    Returns:
        ReplyKeyboardMarkup: Объект реплай-клавиатуры для выбора города.
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
    """    Creates a reply keyboard with buttons in a single row.

    Args:
        items (list[str] | str): A list of texts for the buttons or a single text for the button.

    Returns:
        ReplyKeyboardMarkup: The reply keyboard object.
    """
    if isinstance(items, str):
        items = [items]

    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)
