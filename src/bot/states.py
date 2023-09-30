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
    # # Config
    create_lesson_filter = State()
    filter_order = State()
    filter_type = State()
    filter_level = State()
    filter_status = State()
    # # Watch
    watch_lesson = State()
    # # Edit
    edit_lesson = State()
    edit_lesson_type = State()
    edit_lesson_level = State()
    edit_lesson_status = State()


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
