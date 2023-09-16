from datetime import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.bot.enums import UserLevel
from src.bot.keyboards import buttons_menu
from src.bot.models import UserModel
from src.bot.states import MenuState
from src.infrastructure.database import cursor
from src.infrastructure.logger_builder import build_logger


logger = build_logger(__name__)


async def cmd_start(message: Message) -> None:
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

        else:
            say_hello = "Hello again! ^^"

        await message.answer(
            say_hello,
            reply_markup=ReplyKeyboardRemove(),
        )

    else:
        await message.answer("Hello %username%.")


async def cmd_menu(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    document: dict = cursor.users.find_one({"user_id": user_id})

    if document:
        user_obj = UserModel.model_validate(document)

        if user_obj.level in [UserLevel.SUPERUSER, UserLevel.ADMIN, UserLevel.MODERATOR, UserLevel.MEMBER]:
            await state.clear()
            await state.set_state(MenuState.start_menu)
            await message.answer("Let's make some bachata!", reply_markup=buttons_menu())

        else:
            await state.clear()
            await message.answer(
                "Hmm...\nI don't see you in white list.\n\n<i>Contact the admin (@RoTor_Ex) to gain access</i>.",
                reply_markup=ReplyKeyboardRemove(),
            )

    else:
        await message.answer("Who are you? Firstly run `/start` so that I can indentify you.")
