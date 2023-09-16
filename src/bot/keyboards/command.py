from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def buttons_menu(is_superuser: bool = False) -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text="Info"),
        ],
        [
            KeyboardButton(text="Dance"),
        ],
    ]
    superuser_kb = [
        KeyboardButton(text="Manage"),
    ]

    if is_superuser:
        kb.append(superuser_kb)

    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Bla-bla")

    return keyboard
