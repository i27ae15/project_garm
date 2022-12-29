from graphene_django import DjangoObjectType
from graphene import relay

from user_info.models import CustomUser as User
from user_info.models import FriendRequest


class UserType(DjangoObjectType):
    class Meta:
        model = User
        # exclude = ('profile_photo', 'posts_seen_in_last_24_hours')
        filter_fields = (
            'id',
            'username',
            'email',
            'friends',
        )
        interfaces = (relay.Node, )


class FriendRequestType(DjangoObjectType):
    class Meta:
        model = FriendRequest
        filter_fields = (
            'id',
            'from_user',
            'to_user',
            'accepted_at',
            'created_at',
        )
        interfaces = (relay.Node, )




