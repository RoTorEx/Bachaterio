import random as r
from datetime import datetime

from aiogram.types import ContentType, User
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from src.bot.enums import SelectLessonOrderFilter, SuggestionStatus, UserLevel
from src.bot.models import SuggestionModel, TutorialModel, UserModel
from src.infrastructure.database import cursor


# ======
# COMMON
async def get_dance_data(dialog_manager: DialogManager, **kwargs):
    response = {}

    event_user: User = dialog_manager.middleware_data["event_from_user"]

    document: dict = cursor.users.find_one({"user_id": event_user.id})
    user_obj = UserModel.model_validate(document)

    if user_obj.level in [UserLevel.MODERATOR, UserLevel.ADMIN, UserLevel.SUPERUSER]:
        response.update({"is_moder": True})

    return response


# ====
# LAOD
async def get_load_lesson_data(dialog_manager: DialogManager, **kwargs):
    response = {}

    lesson_date = dialog_manager.dialog_data.get("lesson_date")

    if lesson_date:
        response.update({"lesson_date": lesson_date, "load_lesson": True})

    else:
        response.update({"say_sorry": True})

    return response


# ========
# PRACTICE
async def get_lesson_filter_data(dialog_manager: DialogManager, **kwargs) -> dict:
    response = {
        "lesson_order": dialog_manager.dialog_data["lesson_order"],
        "lesson_type": dialog_manager.dialog_data["lesson_type"],
        "lesson_level": dialog_manager.dialog_data["lesson_level"],
    }

    return response


async def get_lesson_data(dialog_manager: DialogManager, **kwargs):
    response = {}

    skip_stamp = dialog_manager.dialog_data["skip_stamp"]
    sorting_order = dialog_manager.dialog_data["sorting_order"]
    query = dialog_manager.dialog_data["query"]

    tutorial = None
    count = cursor.tutorials.count_documents(query)
    dialog_manager.dialog_data["count"] = count

    if sorting_order == SelectLessonOrderFilter.SINGLE:
        result = cursor.tutorials.find_one(query)

        if result:
            tutorial = TutorialModel.model_validate(result)

    elif sorting_order == SelectLessonOrderFilter.RANDOM:
        unique_ids = cursor.tutorials.find(query).distinct("tg_unique_file_id")

        if unique_ids:
            unique_id = r.choice(unique_ids)
            document = cursor.tutorials.find_one({"tg_unique_file_id": unique_id})
            tutorial = TutorialModel.model_validate(document)
            response.update({"random": True})

    else:
        # Define default values
        sort_arg = "lesson_date"
        sort_value = -1

        if sorting_order in [SelectLessonOrderFilter.NEWEST, SelectLessonOrderFilter.OLDEST]:
            sort_value = -1 if sorting_order == SelectLessonOrderFilter.NEWEST else 1

        elif sorting_order in [SelectLessonOrderFilter.LAST_LOADED, SelectLessonOrderFilter.FIRST_LOADED]:
            sort_value = -1 if sorting_order == SelectLessonOrderFilter.LAST_LOADED else 1
            sort_arg = "created_at"

        result = list(cursor.tutorials.find(query).sort([(sort_arg, sort_value), ("_id", 1)]).skip(skip_stamp).limit(1))

        if result:
            document: dict = result[-1]
            tutorial = TutorialModel.model_validate(document)
            response.update({"order": True})

    event_user: User = dialog_manager.middleware_data["event_from_user"]

    document: dict = cursor.users.find_one({"user_id": event_user.id})
    user_obj = UserModel.model_validate(document)

    if user_obj.level in [UserLevel.MODERATOR, UserLevel.ADMIN, UserLevel.SUPERUSER]:
        response.update({"is_moder": True})

    if tutorial:
        lesson_video = MediaAttachment(ContentType.VIDEO, file_id=MediaId(tutorial.tg_file_id))

        response.update(
            {
                "current": skip_stamp + 1,
                "count": count,
                "show_lesson": True,
                "lesson_video": lesson_video,
                "lesson_id": tutorial.id,
                "lesson_date": tutorial.lesson_date.strftime("%d/%m/%Y"),
                "lesson_type": tutorial.lesson_type.value if tutorial.lesson_type else "null",
                "lesson_level": tutorial.lesson_level.value if tutorial.lesson_level else "null",
                "lesson_description": tutorial.lesson_description,
            }
        )
        dialog_manager.dialog_data["tg_unique_file_id"] = tutorial.tg_unique_file_id

    else:
        response = {
            "say_sorry": True,
        }

    return response


async def get_edit_lesson_data(dialog_manager: DialogManager, **kwargs):
    response = {}

    unique_file_id = dialog_manager.dialog_data["tg_unique_file_id"]
    suggestion_id = dialog_manager.dialog_data["suggestion_id"]

    document: dict = cursor.tutorials.find_one({"tg_unique_file_id": unique_file_id})

    tutorial = TutorialModel.model_validate(document)
    lesson_video = MediaAttachment(ContentType.VIDEO, file_id=MediaId(tutorial.tg_file_id))

    event_user: User = dialog_manager.middleware_data["event_from_user"]

    document: dict = cursor.users.find_one({"user_id": event_user.id})
    user_obj = UserModel.model_validate(document)

    if user_obj.level in [UserLevel.ADMIN, UserLevel.SUPERUSER]:
        response.update({"is_admin": True})

    edit_document = cursor.suggestions.find_one({"id": suggestion_id})

    if not edit_document:
        event_user: User = dialog_manager.middleware_data["event_from_user"]
        suggest_obj = SuggestionModel(
            id=suggestion_id,
            tutorial_id=tutorial.id,
            tg_unique_file_id=tutorial.tg_unique_file_id,
            edit_lesson_description=tutorial.lesson_description,
            edit_lesson_date=tutorial.lesson_date,
            edit_lesson_type=tutorial.lesson_type,
            edit_lesson_level=tutorial.lesson_level,
            suggestion_status=SuggestionStatus.PENDING,
            suggested_by=event_user.id,  # ToDo: fixit
            is_active=False,
            created_at=datetime.utcnow(),
        )

        edit_document = cursor.suggestions.find_one_and_update(
            {"id": str(suggestion_id)}, {"$set": suggest_obj.model_dump()}, upsert=True, return_document=True
        )

    edit_tutorial = SuggestionModel.model_validate(edit_document)

    response.update(
        {
            # Static
            "lesson_video": lesson_video,
            "lesson_id": tutorial.id,
            "lesson_date": tutorial.lesson_date.strftime("%d/%m/%Y"),
            "lesson_type": tutorial.lesson_type.value if tutorial.lesson_type else "null",
            "lesson_level": tutorial.lesson_level.value if tutorial.lesson_level else "null",
            "lesson_description": tutorial.lesson_description,
            # Dinamic
            "edit_lesson_date": edit_tutorial.edit_lesson_date.strftime("%d/%m/%Y"),
            "edit_lesson_type": edit_tutorial.edit_lesson_type.value if edit_tutorial.edit_lesson_type else "null",
            "edit_lesson_level": edit_tutorial.edit_lesson_level.value if edit_tutorial.edit_lesson_level else "null",
            "edit_lesson_description": edit_tutorial.edit_lesson_description,
        }
    )

    return response
