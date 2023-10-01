from enum import Enum


class SelectLessonOrderFilter(str, Enum):
    NEWEST = "newest"
    OLDEST = "oldest"
    RANDOM = "🎲"
    LAST_LOADED = "last loaded"
    FIRST_LOADED = "first loaded"
    SINGLE = "single"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class SelectLessonTypeFilter(str, Enum):
    ALL = "all"
    ELEMENT = "element"
    COMBINATION = "combination"
    DANCE = "dance"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class SelectLessonLevelFilter(str, Enum):
    ALL = "all"
    NOVICE = 1
    BEGINNER = 2
    INTERMEDIATE = 3
    ADVANCED = 4
    EXPERT = 5

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class SelectLessonStatusFilter(str, Enum):
    DISABLE = "disable"
    ENABLE = "enable"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
