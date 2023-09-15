from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def buttons_menu() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text="Load"),
            KeyboardButton(text="Practice"),
        ],
        [
            KeyboardButton(text="Coming soon..."),
        ],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=":D")

    return keyboard
