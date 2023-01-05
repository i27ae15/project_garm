import graphene
from graphene_file_upload.scalars import Upload


class PostInput(graphene.InputObjectType):
    author = graphene.Int()
    shared_from = graphene.Int()
    parent = graphene.Int()
    
    # post_type = graphene.String()
    can_be_shared = graphene.Boolean()
    description = graphene.String()
    visibility_type = graphene.String()
    
    image = Upload()
    video = Upload()


class PostCommentInput(graphene.InputObjectType):
    author = graphene.Int()
    post = graphene.Int()
    answer_to = graphene.Int()

    comment = graphene.String()