from graphene_django import DjangoObjectType
from graphene import relay

from challenges.models import ChallengePost, ChallengePostComment, Challenge


class ChallengeType(DjangoObjectType):
    class Meta:
        model = Challenge
        filter_fields = {
            'id': ['exact'],
            'created_at': ['exact', 'lt', 'gt'],
            'name': ['exact', 'icontains', 'istartswith'],
            'description': ['exact', 'icontains', 'istartswith'],
        }

        interfaces = (relay.Node, )


class ChallengePostType(DjangoObjectType):
    class Meta:
        model = ChallengePost
        filter_fields = {
            'id': ['exact'],
            'created_at': ['exact', 'lt', 'gt'],

            # Foreign Keys
            'owner__id': ['exact'],
            'challenge__id': ['exact'],
            'challenge__name': ['exact'],
        }

        interfaces = (relay.Node, )


class ChallengePostCommentType(DjangoObjectType):
    class Meta:
        model = ChallengePostComment
        filter_fields = {
            'id': ['exact'],
            'created_at': ['exact', 'lt', 'gt'],
            
            # Foreign Keys
            'owner__id': ['exact'],
            'challenge_post__id': ['exact'],
            'challenge_post__challenge__id': ['exact'],
            'challenge_post__challenge__name': ['exact'],
        }

        interfaces = (relay.Node, )