import random as r

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def choosen_dance_module() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text="Load"),
            KeyboardButton(text="Practice"),
        ],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=":D")

    return keyboard


def finished_lesson_loading() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Done ✔️"), KeyboardButton(text="Edit ✏️")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Show me what you know!")

    return keyboard


def finished_filter_setup() -> ReplyKeyboardMarkup:
    emoji_on_button = r.choice(["🕺", "💃"])

    kb = [
        [KeyboardButton(text=emoji_on_button)],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Be ready!")

    return keyboard
