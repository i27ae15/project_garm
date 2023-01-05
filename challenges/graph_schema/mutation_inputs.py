import graphene


class ChallengePostInput(graphene.InputObjectType):
    owner = graphene.Int()
    description = graphene.String()


class ChallengePostCommentInput(graphene.InputObjectType):
    owner = graphene.Int()
    challenge_post = graphene.Int()
    comment = graphene.String()