import graphene
from django import forms

from users.models import CustomUser, TestForImage

class FriendRequestInput(graphene.InputObjectType):
    from_user = graphene.Int() # I guess this can be gotten from the token, but I'm not sure
    to_user = graphene.Int()


class CreateImageTest(forms.ModelForm):
    class Meta:
        model = TestForImage
        fields = [
            "name",
            "logo",
        ]