import json
import logging

from aiogram import Bot
from aiogram.types.error_event import ErrorEvent
from aiogram.utils.text_decorations import html_decoration as hd
from aiogram_dialog import DialogManager


logger = logging.getLogger(__name__)


async def on_unknown_intent(event: ErrorEvent, dialog_manager: DialogManager) -> None:
    """Example of handling UnknownIntent Error and starting new dialog."""
    logger.error("Restarting dialog: %s", event.exception)
    await dialog_manager.reset_stack()


async def on_unknown_state(event: ErrorEvent, dialog_manager: DialogManager) -> None:
    """Example of handling UnknownState Error and starting new dialog."""
    logger.error("Restarting dialog: %s", event.exception)
    await dialog_manager.reset_stack()


async def handle(error: ErrorEvent, log_chat_id: int, bot: Bot):
    logger.exception(
        "Cause unexpected exception %s, by processing %s",
        error.exception.__class__.__name__,
        error.update.model_dump(exclude_none=True),
        exc_info=error.exception,
    )

    if not log_chat_id:
        return

    await bot.send_message(
        chat_id=log_chat_id,
        text=f"Got exception {hd.quote(str(error.exception))}\n"
        f"during processing "
        f"{hd.quote(json.dumps(error.update.model_dump(exclude_none=True), default=str)[:3500])}\n",
    )

    chat_id: int = error.update.model_dump(exclude_none=True)["message"]["chat"]["id"]

    await bot.send_message(chat_id=chat_id, text="Something went wrong 🥴")
