from enum import Enum


class LessonType(str, Enum):
    ELEMENT = "element"
    COMBINATION = "combination"
    DANCE = "dance"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class LessonStatus(str, Enum):
    DISABLE = "disable"
    ENABLE = "enable"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class LessonLevel(str, Enum):
    NOVICE = 1
    BEGINNER = 2
    INTERMEDIATE = 3
    ADVANCED = 4
    EXPERT = 5

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class SuggestionStatus(str, Enum):
    PENDING = "pending"
    ACCEPT = "accept"
    REJECT = "reject"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
