from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def finish_lesson_loading() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Done ✔️"), KeyboardButton(text="Edit ✏️")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Show me what you know!")

    return keyboard
