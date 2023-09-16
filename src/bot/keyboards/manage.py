from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def choosen_manage_module() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text="Manage users"),
        ],
        [
            KeyboardButton(text="Manage suggestions"),
        ],
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="GOD mode activated!")

    return keyboard
