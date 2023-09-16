from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram_dialog import DialogManager, StartMode

from src.bot.keyboards import choosen_manage_module
from src.bot.states import LoaderState, ManageUserDialog, MenuState
from src.bot.utils import superuser_check
from src.infrastructure.database import cursor
from src.infrastructure.logger_builder import build_logger


logger = build_logger(__name__)


# ======
# Common
@superuser_check
async def msg_select_manage(message: Message, state: FSMContext, bot: Bot, dialog_manager: DialogManager) -> None:
    await state.set_state(MenuState.start_manage)
    await message.answer(
        "Go ahead.",
        reply_markup=choosen_manage_module(),
    )


# ===
# CRM
async def msg_manage_users(message: Message, state: FSMContext, dialog_manager: DialogManager) -> None:
    await message.answer(
        "Here is users list",
        reply_markup=ReplyKeyboardRemove(),
    )

    count = cursor.users.count_documents({})

    await dialog_manager.start(
        ManageUserDialog.manage_users,
        mode=StartMode.RESET_STACK,
        data={
            "skip_stamp": 0,
            "count": count
        },
    )


# ===========
# SUGGESTIONS
async def msg_manage_suggestions(message: Message, state: FSMContext, dialog_manager: DialogManager) -> None:
    await message.answer(
        "Not implemented yet :'(",
    )
