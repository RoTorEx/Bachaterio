from datetime import datetime

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram_dialog import DialogManager, StartMode

from src.bot.enums import UserLevel
from src.bot.models import UserModel
from src.bot.states import MenuDialog
from src.infrastructure.config_reader import settings
from src.infrastructure.database import cursor
from src.infrastructure.logger_builder import build_logger


logger = build_logger(__name__)


async def cmd_start(message: Message, bot: Bot) -> None:
    user_id = message.from_user.id
    document: dict = cursor.users.find_one({"user_id": user_id})

    if not document:
        is_new = True
        user_obj = UserModel(
            user_id=user_id,
            is_bot=message.from_user.is_bot,
            chat_id=message.chat.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
            level=UserLevel.STRANGER,
            created_at=datetime.utcnow(),
        )

        logger.info(f"New user with `{user_id}` ID has been created!")

    else:
        is_new = False
        user_obj = UserModel.model_validate(document)

        user_obj.first_name = message.from_user.first_name
        user_obj.last_name = message.from_user.last_name
        user_obj.username = message.from_user.username

        logger.info(f"User with `{user_id}` ID has been updated!")

    document: dict = cursor.users.find_one_and_update(
        {"user_id": user_obj.user_id},
        {"$set": user_obj.model_dump()},
        return_document=True,
        upsert=True,
    )

    user_obj = UserModel.model_validate(document)

    if message.from_user:
        if is_new:
            say_hello = (
                f"Hi there <i>{user_obj.first_name}</i>.\nSee the available commands by pressing the blue button."
            )

            first_name = user_obj.first_name if user_obj.first_name else ""
            last_name = user_obj.last_name if user_obj.last_name else ""
            username = f"@{user_obj.username}" if user_obj.username else ""

            full_name = first_name + last_name

            await bot.send_message(
                chat_id=settings.tg_bot.info_chat,
                text=(
                    f"New user <i>{full_name}</i> with ID <i>{user_obj.user_id}</i> aka."
                    + f" <i>{username}</i> has registered."
                ),
            )

        else:
            say_hello = "Hello again! ^^\nTap blue button to see all available commands."

        await message.answer(say_hello, reply_markup=ReplyKeyboardRemove())

    else:
        await message.answer("Hello %username%.", reply_markup=ReplyKeyboardRemove())


async def cmd_menu(message: Message, state: FSMContext, dialog_manager: DialogManager) -> None:
    await message.answer(text="Ah shit, here we go again.", reply_markup=ReplyKeyboardRemove())

    await dialog_manager.start(
        MenuDialog.init,
        mode=StartMode.RESET_STACK,
    )


async def cmd_help(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Hmm...\n\n<i>Write to `@RoTor_Ex` if you have any questions</i>.",
        reply_markup=ReplyKeyboardRemove(),
    )
