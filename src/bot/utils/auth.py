from functools import wraps

from aiogram.types import Message

from src.bot.enums import UserLevel
from src.bot.models import UserModel
from src.infrastructure.database import cursor


def superuser_check(f):
    @wraps(f)
    async def decorator(*args, **kwargs):
        message: Message = args[0]

        user_id = message.from_user.id
        document: dict = cursor.users.find_one({"user_id": user_id})
        user_obj = UserModel.model_validate(document)

        if user_obj.level in [UserLevel.SUPERUSER]:
            return await f(*args, **kwargs)

        else:
            await message.answer("You have not access to use `Manage` module.", disable_notification=True,)

    return decorator
