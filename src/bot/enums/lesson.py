from enum import Enum


# ToDo: move `all` in filters

class BachataLessonType(str, Enum):
    ALL = "all"
    ELEMENT = "element"
    COMBINATION = "combination"
    DANCE = "dance"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class BachataLessonStatus(str, Enum):
    DISABLE = "disable"
    ENABLE = "enable"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class BachataLessonLevel(str, Enum):
    ALL = "all"
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
