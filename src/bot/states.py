from aiogram.fsm.state import State, StatesGroup


# Main menu
class MenuDialog(StatesGroup):
    init = State()


# Dance
class InfoDialog(StatesGroup):
    start = State()


# Dance
class DanceDialog(StatesGroup):
    start = State()
    # New lesson
    select_lesson_date = State()
    load_lesson = State()
    # Bachata practice
    create_lesson_filter = State()
    watch_lesson = State()
    edit_lesson = State()


# Rules
class RulesDialog(StatesGroup):
    start = State()


# Superintend
class SuperintendDialog(StatesGroup):
    start = State()
    # Users
    manage_users = State()
    update_user_level = State()
    send_message = State()
    # Suggestions
    manage_suggestions = State()
