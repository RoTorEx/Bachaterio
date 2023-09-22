from aiogram.fsm.state import State, StatesGroup


class MenuState(StatesGroup):
    init = State()
    get_info = State()
    start_dance = State()
    start_manage = State()


# Main menu
class MenuDialog(StatesGroup):
    init = State()


# Dance
class InfoDialog(StatesGroup):
    start = State()


# Dance
class DanceDialog(StatesGroup):
    start = State()
    # Load
    select_lesson_date = State()
    load_lesson = State()
    # Practice
    create_lesson_filter = State()
    watch_lesson = State()
    edit_lesson = State()


# Dance
class RulesDialog(StatesGroup):
    start = State()


# Superintend
class SuperintendDialog(StatesGroup):
    start = State()

    manage_users = State()
    update_user_level = State()

    manage_suggestions = State()


class LoaderState(StatesGroup):
    select_date = State()
    start_load = State()


class PracticeState(StatesGroup):
    setup_filters = State()
    start_watch = State()


class SetupLessonsSelectDialog(StatesGroup):
    setup = State()


class WatchLessonDialog(StatesGroup):
    watch = State()


class EditSubWatchLessonDialog(StatesGroup):
    edit = State()


class ManageUserDialog(StatesGroup):
    manage_users = State()


class SetLevelSubManageUserDialog(StatesGroup):
    set_level = State()
