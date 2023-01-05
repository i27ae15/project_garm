from rest_framework import serializers

from posts.models import Post, PostComment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'deleted_at', 'popularity',)


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'deleted_at',)