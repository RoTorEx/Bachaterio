from functools import partial

from aiogram import F, Router
from aiogram.filters import Command, ExceptionTypeFilter
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState

from src.bot.states import LoaderState, MenuState, PracticeState
from src.bot.views.commands import MENU_COMMAND, START_COMMAND
from src.infrastructure.config_reader import settings

from .apprentice import msg_setup_select_config, msg_start_show_lessons
from .commands import cmd_menu, cmd_start
from .errors import handle, on_unknown_intent, on_unknown_state
from .loader import msg_edit_date, msg_finish_load, msg_save_lesson_videos, msg_save_lessons


def load_handlers() -> Router:
    router = Router(name=__name__)

    # Errors
    router.errors.register(on_unknown_intent, ExceptionTypeFilter(UnknownIntent))
    router.errors.register(on_unknown_state, ExceptionTypeFilter(UnknownState))
    router.errors.register(partial(handle, log_chat_id=settings.tg_bot.log_chat))

    # All commands handlers
    router.message.register(cmd_start, Command(commands=START_COMMAND))
    router.message.register(cmd_menu, Command(commands=MENU_COMMAND))

    # Loader sub-app
    router.message.register(msg_save_lessons, MenuState.start_menu, F.text == F.text == "Load")
    router.message.register(msg_finish_load, LoaderState.start_load, F.text == "Done ✔️")
    router.message.register(msg_edit_date, LoaderState.start_load, F.text == "Edit ✏️")
    router.message.register(msg_save_lesson_videos, LoaderState.start_load)

    # Apprentice sub-app
    router.message.register(msg_setup_select_config, MenuState.start_menu, F.text == "Practice")
    router.message.register(msg_start_show_lessons, PracticeState.setup_filters, F.text.in_({"🕺", "💃"}))

    return router
