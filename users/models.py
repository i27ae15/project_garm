import datetime
import sys
import secrets

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Specie(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Race(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    
    # foreignkeys     
    specie:Specie = models.ForeignKey(Specie, null=True, default=None, on_delete=models.CASCADE)
    race:Race = models.ForeignKey(Race, null=True, default=None, on_delete=models.CASCADE)
    
    # --- many to many ----
    
    friends = models.ManyToManyField('self', blank=True)
    followers = models.ManyToManyField('self', blank=True)
    following = models.ManyToManyField('self', blank=True)

    # -----------------------------------------------------------
    # fields
 
    email:str = models.EmailField(max_length=255, unique=True)
    education = models.CharField(max_length=255, null=True, blank=True)

    first_name:str = models.CharField(max_length=255)
        
    is_active:bool = models.BooleanField(default=True)
    is_staff:bool = models.BooleanField(default=False)
    is_tester:bool = models.BooleanField(default=False)
    is_email_confirmed:bool = models.BooleanField(default=False)
        
    last_name:str = models.CharField(max_length=255)
    
    # objects = CustomUserManager()
    
    phone:str = models.CharField(max_length=120, default='')

    registration_date:datetime.datetime = models.DateTimeField(default=timezone.now)
    
    username:str = models.CharField(max_length=255, unique=True)

    sex:str = models.CharField(max_length=1, null=True, default=None)
        
    code_to_confirm_email:str = models.CharField(null=True, max_length=126)

    # profile_photo = models.ImageField(upload_to='profile_photos', null=True, blank=True)

    job:models.CharField = models.CharField(max_length=255, null=True, blank=True, default=None)

    posts_seen_in_last_24_hours:list[dict] = models.JSONField(default=list)

    """
        The list of post seen is going to have this structure

        [{
            "post_id[int]": 1,
            "time_seen[datetime]": "2021-05-05T12:00:00"
        }]

    """

    # USER PERMISSIONS 
    
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]


    # --- class Properties ---


    @property
    def num_friends(self) -> int:
        return self.friends.count()

    
    @property
    def num_followers(self) -> int:
        return self.followers.count()

    
    @property
    def num_following(self) -> int:
        return self.following.count()
    

    # ------- public class methods ----------

    # this function must be called every 24 hours, 
    # dunno why I created this
    def delete_post_with_more_than_24_hours(self):
        if self.posts_seen_in_last_24_hours:
            for post in self.posts_seen_in_last_24_hours:
                if timezone.now() - post['time_seen'] > datetime.timedelta(days=1):
                    self.posts_seen_in_last_24_hours.remove(post)
            self.save()


    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


    def get_short_name(self):
        return self.username
    
    
    def confirmed_email(self):
        self.code_to_confirm_email = None
        self.is_email_confirmed = True
        self.save()


    def __str__(self):
        return f'{self.id} - {self.email}'

        
    def save(self, *args, **kwargs):
        if not self.pk:
            pass
            if 'test' in sys.argv:
                self.is_tester = True
                self.is_email_confirmed = True

            else:
                self.code_to_confirm_email = secrets.token_urlsafe(21)

                # SendEmail(
                #     send_to=self.email,
                #     subject='please, confirm your email',
                #     html=f'<a href=http://127.0.0.1:5173/confirm-email/{self.code_to_confirm_email}>Confirm you email here</a>'
                # )


        super().save(*args, **kwargs)


class FriendRequest(models.Model):

    """
    This is going to be a model to save the friend request
    """

    from_user:CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friend_requests_sent')
    to_user:CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friend_requests_received')

    # log fields

    accepted_at:datetime.datetime = models.DateTimeField(null=True, blank=True)
    created_at:datetime.datetime = models.DateTimeField(default=timezone.now)


    def mark_as_accepted(self):
        self.accepted_at = timezone.now()
        self.from_user.friends.add(self.to_user)
        # self.to_user.increase_friends(self.from_user)
        
        self.save()


    # when a friend request is created, create a function that notifies the user

    def __str__(self):
        return f'{self.from_user} -> {self.to_user}'



class TestForImage(models.Model):

    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='test_images', null=True, blank=True)

    def __str__(self):
        return f'{self.logo}'