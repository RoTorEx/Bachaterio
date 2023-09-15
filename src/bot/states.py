from aiogram.fsm.state import State, StatesGroup


class MenuState(StatesGroup):
    start_menu = State()
    end_menu = State()


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
