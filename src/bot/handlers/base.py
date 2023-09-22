from functools import partial

from aiogram import Router
from aiogram.filters import Command, ExceptionTypeFilter
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState

from src.bot.views.commands import MENU_COMMAND, START_COMMAND, HELP_COMMAND
from src.infrastructure.config_reader import settings

from .commands import cmd_menu, cmd_start, cmd_help
from .errors import handle, on_unknown_intent, on_unknown_state


def load_handlers() -> Router:
    router = Router(name=__name__)

    # Errors
    router.errors.register(on_unknown_intent, ExceptionTypeFilter(UnknownIntent))
    router.errors.register(on_unknown_state, ExceptionTypeFilter(UnknownState))
    router.errors.register(partial(handle, log_chat_id=settings.tg_bot.log_chat))

    # All commands handlers
    router.message.register(cmd_start, Command(commands=START_COMMAND))
    router.message.register(cmd_menu, Command(commands=MENU_COMMAND))
    router.message.register(cmd_help, Command(commands=HELP_COMMAND))

    return router
