import graphene
from graphene_file_upload.scalars import Upload
from graphene_django.utils import camelize

from graphql.execution.base import ResolveInfo
from graphql_auth.bases import Output

from .query_schema import PostType, PostCommentType
from .mutation_inputs import PostCommentInput, PostInput

from posts.serializers.model_serializers import PostSerializer, PostCommentSerializer


from print_pp.logging import Print


class PostErrorType(graphene.Scalar):
    @staticmethod
    def serialize(errors):
        Print('errors', errors)
        return camelize(errors)


class CreatePost(graphene.Mutation):
    class Arguments:
        input = PostInput(required=True)

    post = graphene.Field(PostType)
    errors = graphene.Field(PostErrorType)

    @classmethod
    def mutate(cls, root, info, input):
        serializer = PostSerializer(data=input)
        if not serializer.is_valid():
            return cls(errors=serializer.errors)

        serializer.save()
        post = serializer.instance

        return CreatePost(post=post)


class PostCommentErrorType(graphene.Scalar):
    @staticmethod
    def serialize(errors):
        return camelize(errors)


class CreatePostComment(graphene.Mutation):
    class Arguments:
        input = PostCommentInput(required=True)

    post_comment = graphene.Field(PostCommentType)
    errors = graphene.Field(PostCommentErrorType)

    @classmethod
    def mutate(cls, root, info, input):
        serializer = PostCommentSerializer(data=input)

        if not serializer.is_valid():
            return cls(errors=serializer.errors)

        serializer.save()
        post_comment = serializer.instance

        return CreatePostComment(post_comment=post_comment)