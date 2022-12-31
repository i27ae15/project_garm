from enum import Enum
from django.db import models


class UserInteractionActionEnum(models.IntegerChoices):
    FOLLOW = 1
    UNFOLLOW = 2
    BLOCK = 3
    UNBLOCK = 4
    REPORT = 5
    UNREPORT = 6
    LIKE = 7
    UNLIKE = 8
    ADD_FRIEND = 9
    REMOVE_FRIEND = 10
    COMMENT = 11
    ANSWER_COMMENT = 12
    DELETE_COMMENT = 13
    TAG = 14


class ActionScoreEnum(Enum):
    FOLLOW = 5
    FRIENDSHIP = 5
    VIEW_PROFILE = 0.5
    LIKE = 0.5
    COMMENT = 1
    TAG = 1