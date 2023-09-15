import random as r

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def finish_filter_setup() -> ReplyKeyboardMarkup:
    emoji_on_button = r.choice(["🕺", "💃"])

    kb = [
        [KeyboardButton(text=emoji_on_button)],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Be ready!")

    return keyboard
