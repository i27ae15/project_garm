# python
import datetime

# django
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# rest_framework
from graphql_jwt import exceptions

# other models
from users.models import CustomUser as User

from print_pp.logging import Print

# Create your models here.


class Challenge(models.Model):
    name:str = models.CharField(max_length=50)
    description:str = models.TextField()
    
    image = models.ImageField(upload_to='challenges/images', null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ChallengePost(models.Model):
    
    #  Foreign Keys
    owner:User = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenge_post_owner')
    challenge:Challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='challenge_post')

    # Many to many
    likes = models.ManyToManyField(User, related_name='challenge_posts_likes', blank=True)

    # fields
    image = models.ImageField(upload_to='challenges/posts', null=True)
    
    created_at:str = models.DateTimeField()

    description:str = models.TextField(default='')

    # properties
    @property
    def num_likes(self) -> int:
        return self.likes.count()
    

    def save(self, *args, **kwargs):
        if not self.pk:
            self.__validate()
            self.created_at = timezone.now()
        super().save(*args, **kwargs)


    def __validate(self):
        
        if ChallengePost.objects.filter(owner=self.owner.pk, challenge=self.challenge.pk).count() > 0:
            raise Exception('You already have a post for this challenge')


    def __str__(self):
        return self.challenge.name
    

class ChallengePostComment(models.Model):
    
    # Foreign Keys
    owner:User = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenge_post_comments')
    challenge_post:ChallengePost = models.ForeignKey(ChallengePost, on_delete=models.CASCADE, related_name='comments')
    
    # Many to many
    likes = models.ManyToManyField(User, related_name='challenge_post_comments_likes', blank=True)

    # fields
    comment:str = models.TextField()
    
    created_at:datetime.datetime = models.DateTimeField()
    
    # properties
    @property
    def num_likes(self) -> int:
        return self.likes.count()


    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.comment[:20]


class ChallengeOfTheDay(models.Model):
    challenge:Challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='challenge_of_the_day')
    challenge_post_winner:ChallengePost = models.ForeignKey(ChallengePost, on_delete=models.CASCADE, related_name='challenge_of_the_day', null=True, default=None)

    date = models.DateField()    

    @property
    def challenge_winner(self) -> User:
        return self.challenge_post_winner.owner


    def save(self, *args, **kwargs):
        if not self.pk:
            self.date = timezone.now().date()
        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.date} - {self.challenge.name}'



