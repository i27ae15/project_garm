import graphene

from graphene_django.utils import camelize

from challenges.graph_schema.query_schema import ChallengePostType, ChallengePostCommentType
from challenges.graph_schema.mutation_inputs import ChallengePostCommentInput, ChallengePostInput

from challenges.models import ChallengePost, ChallengePostComment, ChallengeOfTheDay

from challenges.serializers.model_serializers import ChallengePostCommentSerializer, ChallengePostSerializer

from print_pp.logging import Print

from utils.graph_validations import validate_mutation_input

class ChallengesErrorType(graphene.Scalar):
    @staticmethod
    def serialize(errors):
        return camelize(errors)


class CreateChallengePost(graphene.Mutation):
    class Arguments:
        input = ChallengePostInput(required=True)

    challenge_post = graphene.Field(ChallengePostType)
    errors = graphene.Field(ChallengesErrorType)

    # TODO: take the owner from the token

    @classmethod
    def mutate(cls, root, info, input:dict):

        # get todays challenge
        challenge = ChallengeOfTheDay.objects.last().pk
        input['challenge'] = challenge

        # validate input
        is_valid, instance = validate_mutation_input(serializer=ChallengePostSerializer, input=input)
        if not is_valid: return cls(errors=instance)

        return CreateChallengePost(challenge_post=instance)


class CreateChallengePostComment(graphene.Mutation):
    class Arguments:
        input = ChallengePostCommentInput(required=True)

    challenge_post_comment = graphene.Field(ChallengePostCommentType)
    errors = graphene.Field(ChallengesErrorType)

    @classmethod
    def mutate(cls, root, info, input):

        # validate input
        is_valid, instance = validate_mutation_input(serializer=ChallengePostCommentSerializer, input=input)
        if not is_valid: return cls(errors=instance)

        return CreateChallengePostComment(challenge_post_comment=instance)