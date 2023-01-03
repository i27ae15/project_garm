import datetime
import sys
import os
import secrets
from typing import Optional

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import QuerySet

# utils
from .utils.enums import SCORE_OBJECTS, UserInteractionActionEnum, ActionScoreEnum

from print_pp.logging import Print

# we import like this to avoid circular imports

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
    
    phone:str = models.CharField(max_length=120, default='')

    registration_date:datetime.datetime = models.DateTimeField(default=timezone.now)
    
    username:str = models.CharField(max_length=255, unique=True)

    sex:str = models.CharField(max_length=1, null=True, default=None)
        
    code_to_confirm_email:str = models.CharField(null=True, max_length=126)

    profile_photo = models.ImageField(upload_to='profile_photos', null=True, blank=True)

    job:models.CharField = models.CharField(max_length=255, null=True, blank=True, default=None)
    
    interactions_score:int = models.IntegerField(default=0)

    # USER PERMISSIONS 
    
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    # private fields

    interaction_head_with_score:'UserInteraction' = models.ForeignKey('UserInteraction', null=True, default=None, on_delete=models.CASCADE, related_name='interaction_head_with_score')
    interaction_head_without_score:'UserInteraction' = models.ForeignKey('UserInteraction', null=True, default=None, on_delete=models.CASCADE, related_name='interaction_head_without_score')

    interaction_tail_with_score:'UserInteraction' = models.ForeignKey('UserInteraction', null=True, default=None, on_delete=models.CASCADE, related_name='interaction_tail_with_score')
    interaction_tail_without_score:'UserInteraction' = models.ForeignKey('UserInteraction', null=True, default=None, on_delete=models.CASCADE, related_name='interaction_tail_without_score')

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


    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


    def get_short_name(self):
        return self.username
    
    
    def confirmed_email(self):
        self.code_to_confirm_email = None
        self.is_email_confirmed = True
        self.save()

    
    def add_friend(self, user:'CustomUser'):
        self.friends.add(user)
        self.create_new_interaction(user, way_of_initiation=UserInteractionActionEnum.FRIENDSHIP)
        user.create_new_interaction(self, way_of_initiation=UserInteractionActionEnum.FRIENDSHIP)
        self.save()

    
    def create_action(self, user:'CustomUser', action:UserInteractionActionEnum):
        """
        This method is going to create a new action
        """
        # we create the new interaction

        interaction = self.get_interactions(user_id=user.pk).first()
        new_action = interaction.create_action(action=action)
        # we return the new interaction
        return new_action

    
    def traverse_linked_list(self, head:'UserInteraction') -> QuerySet['UserInteraction']:
        """
        This method is going to traverse the linked list of interactions
        """
        # we create a list to store the interactions
        interactions = []

        # we traverse the linked list
        while head:
            interactions.append(head)
            head = head.next_node

        return QuerySet(interactions)


    def equilibrate_score(self, value_to_increase):
        """
        This method is going to equilibrate the score of the interactions
        """
        # we traverse the linked list
        linked_list = self.traverse_linked_list(self.interaction_head_with_score)

        # getting the oldest interaction updated, so we can delete the score to it and 
        # add it to the new interaction        
        interaction:'UserInteraction' = linked_list.order_by('updated_at').first()
        actions:QuerySet['InteractionAction'] = interaction.get_actions(active_actions_for_score=True)
        current = 0

        interaction.save()
        
        while self.interactions_score + value_to_increase > 100:
            if current == len(actions):
                linked_list = self.traverse_linked_list(self.interaction_head_with_score)
                interaction:'UserInteraction' = linked_list.order_by('updated_at').first()
                interaction.save()
                actions:QuerySet['InteractionAction'] = interaction.get_actions(active_actions_for_score=True)
                current = 0
                continue

            action = actions[current]
            action.deactivate()
            current += 1
        
    
    def get_interactions(self, **kwargs) -> QuerySet['UserInteraction']:
        
        if not kwargs:
            return self.interactions_made.all()
        
        if user_id:=kwargs.get('user_id'):
            # we'll start filtering with the score branch
            head = self.interaction_head_with_score
            
            go_to_no_score = True
            
            while True:
                if head.to_user.pk == user_id:
                    return QuerySet(head)
                head = head.next_node
                if not head and go_to_no_score:
                    head = self.interaction_head_without_score
                    go_to_no_score = False
                elif not head and not go_to_no_score:
                    if kwargs.get('fix_errors'):
                        return QuerySet(self.create_new_interaction(CustomUser.objects.get(pk=user_id)))
                    raise Exception(_('The interaction does not exist'))


    def create_new_interaction(self, user:'CustomUser', way_of_initiation=UserInteractionActionEnum) -> 'UserInteraction':
        """
        This method is going to create a new interaction between the user and the user that is passed as argument
        """

        __ways = {
            UserInteractionActionEnum.FRIENDSHIP: {
                'are_friends': True,
                'is_following': True,
            },
            UserInteractionActionEnum.FOLLOW: {
                'is_following': True,
            },
            UserInteractionActionEnum.BLOCK: {
                'is_blocked': True,
            }
        }

        if way_of_initiation not in __ways.keys():
            raise Exception(_('The way of initiation is not valid'))

        # we create the interaction
        interaction = UserInteraction.objects.create(
            from_user=self,
            to_user=user,
            **__ways[way_of_initiation]
        )

        # we create the head and the tail for the interaction with score 
        # we know is an interaction with score because when an interaction is created, by default gets and score of 5
        if not self.interaction_head_with_score:
            self.interaction_head_with_score = interaction
            self.interaction_tail_with_score = interaction

        return interaction


    def set_new_interaction_head(self, node:'UserInteraction', with_score:bool):
        """
        This method is going to set the new head of the user
        """
        if with_score:
            head = self.interaction_head_with_score
        else:
            head = self.interaction_head_without_score

        if head:
            head.is_head = False
            head.previous_node = node
            node.next_node = head

        # setting the new head
        head = node
        head.is_head = True

        # if with_score:
        #     self.interaction_head_with_score = head
        # else:
        #     self.interaction_head_without_score = head

        head.save()
        self.save()


    def set_new_interaction_tail(self, node:'UserInteraction', with_score:bool, save_node=True):
        """
        This method is going to set the new tail of the user
        """
        if with_score:
            tail = self.interaction_tail_with_score
        else:
            tail = self.interaction_tail_without_score
        
        if tail:
            tail.is_tail = False
            tail.next_node = node
            node.previous_node = tail

        # setting the new tail
        tail = node
        tail.is_tail = True

        if with_score:
            self.interaction_tail_with_score = tail
        else:
            self.interaction_tail_without_score = tail

        tail.save(save_node=save_node)
        self.save()


    def validate_interactions_score(self, value_to_increase:int):
        """
        This method is going to validate the interactions of the user
        """ 

        total_score = self.interactions_score + value_to_increase

        if total_score <= 100 or value_to_increase < 0:
            self.interactions_score = total_score
            self.save()
            return
        
        self.equilibrate_score(value_to_increase)


    def save(self, *args, **kwargs):
        if not self.pk:
            pass
            if 'test' in sys.argv or os.environ.get('NO_EMAIL_NOTIFICATIONS'):
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


    def __str__(self):
        return f'{self.pk} - {self.email}'


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


class UserInteraction(models.Model):

    """
    This is going to be a model to save the interactions of the users

    This interaction is created when users interacts with another user, this could be a follow, a profile visit, 
    a like, a comment, etc
    """

    from_user:CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='interactions_made')
    to_user:CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='interactions_received')
    next_node:Optional['UserInteraction'] = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='next_interaction_node')
    previous_node:Optional['UserInteraction'] = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='previous_interaction_node')

    score:float = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(30)])
    is_active:bool = models.BooleanField(default=True) # this is going to be used to deactivate the interaction
    # if one of the user has blocked the other, this will be set to False

    # log fields
    created_at:datetime.datetime = models.DateTimeField(default=timezone.now)
    updated_at:datetime.datetime = models.DateTimeField(auto_now=True)
    started_with = models.IntegerField(choices=[
        (UserInteractionActionEnum.FOLLOW.value, UserInteractionActionEnum.FOLLOW.name),
        (UserInteractionActionEnum.FRIENDSHIP.value, UserInteractionActionEnum.FRIENDSHIP.name)
    ], default=UserInteractionActionEnum.FRIENDSHIP.value)

    comments:str = models.TextField(null=True, blank=True)

    are_friends:bool = models.BooleanField(default=False) # this is going to be used to know if the interaction is a friendship
    is_following:bool = models.BooleanField(default=False) # this is going to be used to know if the interaction is a follow
    is_blocked:bool = models.BooleanField(default=False) # this is going to be used to know if the interaction is a block

    """
    
    from_user(following) -> to_user

    """

    # this is going to be used to know if the interaction is the head or the tail of the user
    is_head:bool = False
    is_tail:bool = False


    # properties
    @property
    def interaction_with_score(self) -> 'UserInteraction':
        return self.score > 0


    @property
    def head(self) -> 'UserInteraction':
        if self.interaction_with_score:
            return self.from_user.interaction_head_with_score
        else:
            return self.from_user.interaction_head_without_score
    

    @property
    def tail(self) -> 'UserInteraction':
        if self.interaction_with_score:
            return self.from_user.interaction_tail_with_score
        else:
            return self.from_user.interaction_tail_without_score


    @property
    def actions(self) -> QuerySet['InteractionAction']:
        return self.interaction_actions.all()

    # methods

    def get_actions(self, active_actions_for_score=False) -> QuerySet['InteractionAction']:
        if not active_actions_for_score: return self.actions.all()
        return self.actions.filter(is_active_for_score=True)


    def remove_node(self):
        if self.is_head:
            self.from_user.set_new_interaction_head(self.next_node, self.interaction_with_score)
        elif self.is_tail:
            self.from_user.set_new_interaction_tail(self.previous_node, self.interaction_with_score)
        else:
            self.previous_node.next_node = self.next_node
            self.next_node.previous_node = self.previous_node
    

    def change_node_from_branch(self):
        """
        This method is going to move the node to the no score branch
        """ 

        # removing the node from the score branch
        self.remove_node()
        self.from_user.set_new_interaction_tail(self, self.interaction_with_score == False)
    

    def decrease_score(self, action_type:UserInteractionActionEnum):
        """
        This method is going to decrease the score of the interaction
        """
        value_to_decrease = action_type.value

        if self.score - value_to_decrease < 0:
            self.score = 0
            value_to_decrease = self.score - value_to_decrease
        else:
            self.score -= value_to_decrease
        
        self.save()

        self.from_user.validate_interactions_score(value_to_decrease)


    def increase_score(self, action_type:UserInteractionActionEnum):
        """
        This method is going to increase the score of the interaction
        """
        value_to_increase = action_type.value

        if self.score + value_to_increase > 30:
            self.score = 30
            value_to_increase = self.score + value_to_increase - 30
        else:
            self.score += value_to_increase
        
        self.save()
        self.from_user.validate_interactions_score(value_to_increase)


    def create_action(self, action:UserInteractionActionEnum) -> 'InteractionAction':
        """
        This method is going to create a new action for the interaction
        """
        return InteractionAction.objects.create(
            interaction=self,
            made_by=self.from_user,
            action=action.value,
            is_first_action=self.actions.count() == 0
        )


    def save(self, save_node=True, *args, **kwargs):
        self.__validate()
        if not save_node: return
        first_time = False
        if not self.pk:
            first_time = True
        super().save(*args, **kwargs)

        if first_time:
            self.is_tail = True
            self.from_user.set_new_interaction_tail(self, with_score=True, save_node=False)
            self.create_action(UserInteractionActionEnum.FRIENDSHIP)
            self.save()


    def __validate(self):
        if not self.pk:
            if not self.are_friends and not self.is_following and not self.is_blocked:
                raise Exception('The interaction must be a friendship, a follow or a block')


    def __str__(self):
        return f'{self.from_user} -> {self.to_user}'


class InteractionAction(models.Model):
    
    interaction:UserInteraction = models.ForeignKey(UserInteraction, on_delete=models.CASCADE, related_name='interaction_actions')
    made_by:CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    # fields

    action:int = models.IntegerField(choices=UserInteractionActionEnum.choices, default=0)
    is_active_for_score:bool = models.BooleanField(default=True)

    # post:Post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    challenge_post = models.ForeignKey('challenges.ChallengePost', null=True, blank=True, on_delete=models.CASCADE)
    # log fields
    
    created_at:datetime.datetime = models.DateTimeField(default=timezone.now)

    is_first_action:bool = models.BooleanField(default=False)

    @property
    def action_enum(self) -> UserInteractionActionEnum:
        
        return UserInteractionActionEnum(self.action)


    def deactivate(self):
        self.is_active_for_score = False
        self.interaction.decrease_score(self.action)
        self.save()


    def save(self, *args, **kwargs):

        is_creation = False

        if not self.pk:
            is_creation = True

        self.__validate(self.made_by, self.interaction)
        super().save(*args, **kwargs)

        # we do this, because we must save the interaction before to increase the score
        if is_creation:
            if self.action_enum in SCORE_OBJECTS:
                self.interaction.increase_score(ActionScoreEnum[self.action_enum.name])
            else:
                self.is_active_for_score = False
                self.save()

    
    def __validate(self, user:CustomUser, interaction:UserInteraction) -> bool:
        if user != interaction.from_user and user != interaction.to_user:
            raise Exception(_('The selected user is not valid, please select a valid user'))
        

        if not self.is_first_action:
            if self.action_enum == UserInteractionActionEnum.FRIENDSHIP and interaction.are_friends:
                raise Exception(_('There is already a friendship action for this interaction'))
        
            if self.action_enum == UserInteractionActionEnum.FOLLOW and interaction.is_following:
                raise Exception(_('There is already a follow action for this interaction'))


        if self.action_enum == UserInteractionActionEnum.BLOCK and interaction.is_blocked:
            raise Exception(_('There is already a block action for this interaction'))
       
       
        return True


    def __str__(self):
        return f'{self.made_by} -> {self.action_enum.name}'


class TestForImage(models.Model):

    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='test_images', null=True, blank=True)

    def __str__(self):
        return f'{self.logo}'

