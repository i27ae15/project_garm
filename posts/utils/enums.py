from django.db import models


class PostVisibilityTypes(models.IntegerChoices):
    PUBLIC = 1
    PRIVATE = 2
    FRIENDS = 3