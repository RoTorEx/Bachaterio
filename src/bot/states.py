from aiogram.fsm.state import State, StatesGroup


class MenuState(StatesGroup):
    init = State()
    get_info = State()
    start_dance = State()
    start_manage = State()


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
