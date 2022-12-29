from rest_framework import serializers
from challenges.models import ChallengePost, ChallengePostComment


class ChallengePostSerializer(serializers.ModelSerializer):

    num_like = serializers.SerializerMethodField()


    def get_num_like(self, instance:ChallengePost):
        return instance.num_likes


    class Meta:
        model = ChallengePost
        fields = '__all__'
        read_only_fields = ('created_at', 'likes')


class ChallengePostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengePostComment
        fields = '__all__'
        read_only_fields = ('created_at', 'likes')