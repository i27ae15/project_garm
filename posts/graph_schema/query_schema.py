from graphene_django import DjangoObjectType
from graphene import relay

from posts.models import Post, PostComment


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        # exclude = ('profile_photo', 'posts_seen_in_last_24_hours')
        filter_fields = (
            'id',
            'author',
            'shared_from',
            'parent',
            'post_type',
            'can_be_shared',
            'description',
            'visibility_type',
            'created_at',
            'updated_at',
            'popularity',
        )
        interfaces = (relay.Node, )


class PostCommentType(DjangoObjectType):
    class Meta:
        model = PostComment
        filter_fields = (
            'id',
            'post',
            'author',
            'comment',
            'created_at',
            'updated_at',
        )
        interfaces = (relay.Node, )