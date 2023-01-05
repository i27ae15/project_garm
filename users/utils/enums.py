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
    FRIENDSHIP = 9
    UNFRIENDSHIP = 10
    COMMENT = 11
    ANSWER_COMMENT = 12
    DELETE_COMMENT = 13
    TAG = 14
    SHARE = 15


class ActionScoreEnum(Enum):
    FOLLOW = 5
    FRIENDSHIP = 5
    VIEW_PROFILE = 0.5
    LIKE = 0.5
    COMMENT = 1
    TAG = 1
    SHARE = 1.5


class LinkedListTypeEnum(Enum):
    WITH_SCORE = 1
    WITHOUT_SCORE = 2


SCORE_OBJECTS = [
    UserInteractionActionEnum.FOLLOW, 
    UserInteractionActionEnum.FRIENDSHIP, 
    UserInteractionActionEnum.LIKE, 
    UserInteractionActionEnum.COMMENT, 
    UserInteractionActionEnum.TAG
]


MAX_SCORE_FOR_INTERACTIONS = 100
MAX_NUM_OF_INTERACTIONS = 10