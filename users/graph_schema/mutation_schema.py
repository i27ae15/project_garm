import graphene

from .query_schema import FriendRequestType

# models
from user_info.models import FriendRequest

# serializers
from user_info.serializers.model_serializers import FriendRequestSerializer

# inputs
from .mutation_inputs import FriendRequestInput

# utils
from print_pp.logging import Print
from graphene_django.utils import camelize


class UserInfoErrorType(graphene.Scalar):
    @staticmethod
    def serialize(errors):
        return camelize(errors)


class CreateFriendRequest(graphene.Mutation):
    class Arguments:
        input = FriendRequestInput(required=True)
    
    friend_request = graphene.Field(FriendRequestType)
    errors = graphene.Field(UserInfoErrorType)


    @classmethod
    def mutate(cls, root, info, input):
        serializer = FriendRequestSerializer(data=input)

        if not serializer.is_valid():
            return cls(errors=serializer.errors)

        serializer.save()
        friend_request = serializer.instance
        Print('friend request', FriendRequest.objects.all())


        return CreateFriendRequest(friend_request=friend_request)


class UpdateFriendRequest(graphene.Mutation):
    class Arguments:
        accepted = graphene.Boolean(required=True)
        id = graphene.ID()

    friend_request = graphene.Field(FriendRequestType)
    ok = graphene.Boolean()


    @classmethod
    def mutate(cls, root, info, accepted, id):
        friend_request = FriendRequest.objects.get(pk=id)
        if accepted:
            friend_request.mark_as_accepted()
        else:
            friend_request.delete()

        return UpdateFriendRequest(friend_request=friend_request, ok=True)
