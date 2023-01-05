# rest_framework
from rest_framework import serializers

from ..models import CustomUser, FriendRequest, TestForImage

# models
# from ..models import UserInteraction


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'email',
            'education',
            'first_name',
            'last_name',
            'is_active',
            'phone',
            'sex',
            'username',
            'profile_photo'
            'job',
        )


class FriendRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendRequest
        fields = '__all__'


class UserDefaultValuesForPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('post_default_visibility', 'post_default_can_be_shared')


class TestForImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestForImage
        fields = '__all__'


# class UserInteractionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserInteraction
#         fields = '__all__'
#         read_only_fields = ('created_at', 'updated_at')