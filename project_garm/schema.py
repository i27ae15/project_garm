import graphene

from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay

from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations

from graphql_auth.decorators import verification_required

from users.graph_schema.mutation_schema import CreateFriendRequest, UpdateFriendRequest, CreateImageSerializer, CreateTestImage
from users.graph_schema.query_schema import FriendRequestType, SpecieType, RaceType
from users.models import Specie, Race, FriendRequest

from posts.graph_schema.mutation_schema import CreatePost, CreatePostComment
from posts.graph_schema.query_schema import PostType, PostCommentType

from challenges.graph_schema.query_schema import ChallengePostType, ChallengePostCommentType
from challenges.graph_schema.mutation_schema import CreateChallengePost, CreateChallengePostComment
from challenges.models import ChallengePost, ChallengePostComment


class AuthMutation(graphene.ObjectType):
    # change this piece of shit to something better
    register = mutations.Register.Field()
    update_account = mutations.UpdateAccount.Field()


    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()


class Query(UserQuery, MeQuery, graphene.ObjectType):
   

    # for challenges -----------------------------------
    challenge_post_l = graphene.List(ChallengePostType)
    challenge_post = relay.Node.Field(ChallengePostType)
    all_challenge_post = DjangoFilterConnectionField(ChallengePostType)

    def resolve_challenge_post_l(self, info, **kwargs):
        return ChallengePost.objects.all()

    challenge_post_comment_l = graphene.List(ChallengePostCommentType)
    challenge_post_comment = relay.Node.Field(ChallengePostCommentType)
    all_challenge_post_comment = DjangoFilterConnectionField(ChallengePostCommentType)


    def resolve_challenge_post_comment_l(self, info, **kwargs):
        return ChallengePostComment.objects.all()
    

    # for posts -----------------------------------------
    post_l = graphene.List(PostType)
    post = relay.Node.Field(PostType)
    all_post = DjangoFilterConnectionField(PostType)

    def resolve_post_l(self, info, **kwargs):
        return PostType.objects.all()

    post_comment_l = graphene.List(PostCommentType)
    post_comment = relay.Node.Field(PostCommentType)
    all_post_comment = DjangoFilterConnectionField(PostCommentType)

    def resolve_post_comment_l(self, info, **kwargs):
        return PostCommentType.objects.all()


    # for users -----------------------------------------
    friend_request_l = graphene.List(FriendRequestType)
    friend_request = relay.Node.Field(FriendRequestType)
    all_friend_request = DjangoFilterConnectionField(FriendRequestType)

    def resolve_friend_request_l(self, info, **kwargs):
        return FriendRequest.objects.all()

    specie_l = graphene.List(SpecieType)
    specie = relay.Node.Field(SpecieType)
    all_specie = DjangoFilterConnectionField(SpecieType)

    def resolve_specie_l(self, info, **kwargs):
        return Specie.objects.all()
    
    race_l = graphene.List(RaceType)
    race = relay.Node.Field(RaceType)
    all_race = DjangoFilterConnectionField(RaceType)
    
    def resolve_race_l(self, info, **kwargs):
        return Race.objects.all()  


class Mutation(AuthMutation, graphene.ObjectType):

    create_image = CreateImageSerializer.Field()

    # user info mutations
    create_friend_request = CreateFriendRequest.Field()
    accept_reject_friend_request = UpdateFriendRequest.Field()

    # challenges mutations
    create_challenge_post = CreateChallengePost.Field()
    create_challenge_post_comment = CreateChallengePostComment.Field()

    # posts mutations
    create_post = CreatePost.Field()
    create_post_comment = CreatePostComment.Field()


# @verification_required


schema = graphene.Schema(query=Query, mutation=Mutation)
