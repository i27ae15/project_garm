# python
import datetime

# django
from django.db.models import QuerySet
from django.db import models
from django.utils import timezone

# other models
from users.models import CustomUser as User

# type classes
from .utils.enums import PostVisibilityTypes

# values
from users.utils.enums import ActionScoreEnum


class Post(models.Model):

    # --- Foreign Keys ---

    author:User = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    shared_from:'Post' = models.ForeignKey('self', on_delete=models.CASCADE, related_name='shares', null=True, default=None)
    parent:'Post' = models.ForeignKey('self', on_delete=models.CASCADE, related_name='post_parent', null=True, default=None)

    # --- Many to many ----
    
    seen_by = models.ManyToManyField(User, related_name='seen_posts', blank=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    users_tagged = models.ManyToManyField(User, related_name='users_tagged', blank=True)
    
    post_type:str = models.CharField(max_length=50, default='post')

    # --------------------
    # ------ Fields ------

    can_be_shared:bool = models.BooleanField(default=True)
    
    description:str = models.TextField(default='')

    image = models.ImageField(upload_to='media_from_users/posts', null=True, default=None)
    
    visibility_type:str = models.IntegerField(choices=PostVisibilityTypes.choices, default=PostVisibilityTypes.PUBLIC)
    video = models.FileField(upload_to='media_from_users/posts', null=True, default=None)

    # Logs fields ------------------------
    created_at:datetime.datetime = models.DateTimeField()
    updated_at:datetime.datetime = models.DateTimeField(null=True, default=None)
    deleted_at:datetime.datetime = models.DateTimeField(null=True, default=None)

    popularity:int = models.IntegerField(default=0)

    """
    The popularity of the post is going to work similar to the score base of the interactions,
    at least for the moment

    Returns:
        _type_: _description_
    """

    # --- class Properties ---

    @property
    def is_shared(self) -> bool:
        return self.shared_from is not None


    @property
    def is_pet_tagged(self) -> bool:
        return self.pets_tagged is not None


    @property
    def num_of_shares(self) -> int:
        return self.shares.count()

    
    @property
    def num_of_comments(self) -> int:
        return self.comments.count()
        
    
    @property
    def num_of_likes(self) -> int:
        return self.likes.count()


    # ---- private class methods ----


    # ---- public class Methods -----

    
    def set_post_popularity(self, save=False):
        popularity = 0
        
        popularity += self.num_of_likes * ActionScoreEnum.LIKE.value
        popularity += self.num_of_comments * ActionScoreEnum.COMMENT.value
        popularity += self.num_of_shares * ActionScoreEnum.SHARE.value

        self.popularity = popularity
    
        if save: self.save()
        
    
    def increase_likes(self, user:User):
        self.likes.add(user)
        # TODO: Create interaction here
        # TODO: Create notification here
        self.save()


    def increase_pets_tagged(self, user:User):
        self.pets_tagged.add(user)
        # TODO: Create interaction here
        # TODO: Create notification here
        self.save()


    def is_post_edited(self) -> bool:
        return self.updated_at is not None


    def update_share_status(self, new_status:bool):
        self.can_be_shared = new_status
        self.save()

    
    def update_visibility_type(self, new_visibility_type:str):
        self.visibility_type = new_visibility_type
        self.save()


    def update_description(self, new_description:str):
        self.description = new_description
        self.save()

    
    def update_seen_by(self, user:User):
        self.seen_by.add(user)
        self.save()


    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        else:
            self.updated_at = timezone.now()
            self.set_post_popularity()
            
        super().save(*args, **kwargs)

    
    def __str__(self):
        return f'{self.pk} - {self.author}'


class PostComment(models.Model):

    # --- Foreign Keys ---
    
    author:User = models.ForeignKey(User, on_delete=models.CASCADE)
    post:Post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    answer_to = models.ForeignKey('self', on_delete=models.CASCADE, related_name='answers', null=True)

    # --- manytomany ---

    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    # --------------------
    # ------ Fields ------

    comment:str = models.TextField()


    # Logs fields ------------------------
    created_at:datetime.datetime = models.DateTimeField()
    updated_at:datetime.datetime = models.DateTimeField(null=True, default=None)
    deleted_at:datetime.datetime = models.DateTimeField(null=True, default=None)


    # --- class Properties ---

    @property
    def is_comment_edited(self) -> bool:
        return self.updated_at is not None

    @property
    def num_of_likes(self) -> int:
        return self.likes.count()

    @property
    def num_of_answers(self) -> int:
        return self.answers.count()

    # ---- Class Methods -----

    def increase_likes(self, user:User) -> None:
        self.likes.add(user)
        # TODO: Create interaction here
        # TODO: Create notification here
        self.save()


    def update_comment(self, new_comment:str) -> None:
        self.comment = new_comment
        # TODO: Create interaction here
        # TODO: Create notification here
        self.save()


    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        else:
            self.updated_at = timezone.now()
        
        super().save(*args, **kwargs)


    def __str__(self):
        return self.comment
