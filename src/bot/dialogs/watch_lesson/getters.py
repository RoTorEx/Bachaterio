import random as r

from aiogram.types import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from src.bot.enums import BachataLessonLevel, BachataLessonType, SelectOrder
from src.bot.models import TutorialModel
from src.infrastructure.database import cursor


async def get_data_watch_dialog(dialog_manager: DialogManager, **kwargs):
    query = {}  # Update with incoming values

    skip_stamp = dialog_manager.start_data["skip_stamp"]
    sorting_order = dialog_manager.start_data["sorting_order"]
    lesson_type = dialog_manager.start_data["lesson_type"]
    lesson_level = dialog_manager.start_data["lesson_level"]
    lesson_status = dialog_manager.start_data["lesson_status"]

    if lesson_type in [BachataLessonType.COMBINATION, BachataLessonType.DANCE, BachataLessonType.ELEMENT]:
        query.update({"lesson_type": lesson_type})

    if lesson_level in [
        BachataLessonLevel.NOVICE,
        BachataLessonLevel.BEGINNER,
        BachataLessonLevel.INTERMEDIATE,
        BachataLessonLevel.ADVANCED,
        BachataLessonLevel.EXPERT,
    ]:
        query.update({"lesson_level": lesson_level})

    query.update({"lesson_status": lesson_status})

    tutorial = None

    if sorting_order == SelectOrder.RANDOM:
        unique_ids = cursor.tutorials.find(query).distinct("tg_unique_file_id")
        if unique_ids:
            unique_id = r.choice(unique_ids)
            document = cursor.tutorials.find_one({"tg_unique_file_id": unique_id})
            tutorial = TutorialModel.model_validate(document)

    else:
        sorting_order = -1 if sorting_order == SelectOrder.NEWEST else 1
        result = (
            cursor.tutorials.find(query).sort([("lesson_date", sorting_order), ("_id", 1)]).skip(skip_stamp).limit(1)
        )

        if result:
            document: dict = list(result)[-1]
            tutorial = TutorialModel.model_validate(document)

    if tutorial:
        lesson_video = MediaAttachment(ContentType.VIDEO, file_id=MediaId(tutorial.tg_file_id))

        watch_lessons_dialog_response = {
            "show_lesson": True,
            "lesson_video": lesson_video,
            "lesson_id": tutorial.tg_unique_file_id,
            "lesson_date": tutorial.lesson_date.strftime("%d/%m/%Y"),
            "lesson_type": tutorial.lesson_type.value if tutorial.lesson_type else "null",
            "lesson_level": tutorial.lesson_level.value if tutorial.lesson_level else "null",
            "lesson_status": tutorial.lesson_status.value,
            "lesson_description": tutorial.lesson_description,
        }
        dialog_manager.start_data["lesson_id"] = tutorial.tg_unique_file_id

    else:
        watch_lessons_dialog_response = {
            "say_sorry": True,
        }

    return watch_lessons_dialog_response
