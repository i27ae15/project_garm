from rest_framework import serializers, fields


class DefaultUserValuesQuerySerializer(serializers.Serializer):
    for_post = fields.BooleanField(default=True, help_text='Si es para un post o no')


class PostQuerySerializer(serializers.Serializer):
    post_id = fields.IntegerField(required=False, help_text='El id del post')
    many = fields.BooleanField(default=False, help_text='Si se quiere traer mas de un post')
    num_of_post = fields.IntegerField(default=10, help_text='El numero de post que se quiere traer')
    most_recent = fields.BooleanField(default=True, help_text='Si se quiere traer los post mas recientes')
    most_likes = fields.BooleanField(default=False, help_text='Si se quiere traer los post con mas likes')


class FriendRequestQuerySerializer(serializers.Serializer):
    sent = fields.BooleanField(default=False, help_text='si se quiere obtener el numero de solicitudes de amistad recibidas, de ser falso trae las recibidas')

    limit = fields.IntegerField(default=10, help_text='El numero de solicitudes de amistad que se quiere traer')