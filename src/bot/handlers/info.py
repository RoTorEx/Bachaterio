from aiogram import Bot, html
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager

from src.bot.models import UserModel
from src.infrastructure.database import cursor
from src.infrastructure.logger_builder import build_logger


logger = build_logger(__name__)


# ======
# Common
async def msg_select_info(message: Message, state: FSMContext, bot: Bot, dialog_manager: DialogManager) -> None:
    user_id = message.from_user.id
    document: dict = cursor.users.find_one({"user_id": user_id})
    user_obj = UserModel.model_validate(document)

    await message.answer(
        "My version: <i>1.0.0</i>\n\n"
        + f"{html.quote('=== < ~ > ===')}\n\n"
        + f"Your ID: <b>{user_id}</b>\n"
        + f"Your level: <b>{user_obj.level.value}</b>",
        disable_notification=True,
    )
