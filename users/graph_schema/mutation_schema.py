import graphene
from graphql.execution.base import ResolveInfo
from graphql_auth.bases import Output
from graphene_file_upload.scalars import Upload


from .query_schema import FriendRequestType

# models
from users.models import FriendRequest

# serializers
from users.serializers.model_serializers import FriendRequestSerializer, TestForImageSerializer

# inputs
from .mutation_inputs import FriendRequestInput, CreateImageTest

# utils
from print_pp.logging import Print
from graphene_django.utils import camelize


class UserInfoErrorType(graphene.Scalar):
    @staticmethod
    def serialize(errors):
        return camelize(errors)


class CreateFriendRequest(graphene.Mutation):
    class Arguments:
        input = FriendRequestInput(required=True)
    
    friend_request = graphene.Field(FriendRequestType)
    errors = graphene.Field(UserInfoErrorType)


    @classmethod
    def mutate(cls, root, info, input):
        serializer = FriendRequestSerializer(data=input)

        if not serializer.is_valid():
            return cls(errors=serializer.errors)

        serializer.save()
        friend_request = serializer.instance
        Print('friend request', FriendRequest.objects.all())


        return CreateFriendRequest(friend_request=friend_request)


class UpdateFriendRequest(graphene.Mutation):
    class Arguments:
        accepted = graphene.Boolean(required=True)
        id = graphene.ID()

    friend_request = graphene.Field(FriendRequestType)
    ok = graphene.Boolean()


    @classmethod
    def mutate(cls, root, info, accepted, id):
        friend_request = FriendRequest.objects.get(pk=id)
        if accepted:
            friend_request.mark_as_accepted()
        else:
            friend_request.delete()

        return UpdateFriendRequest(friend_request=friend_request, ok=True)


class CreateTestImage(graphene.Mutation, Output):
    form = CreateImageTest

    class Arguments:
        """Necessary input to create a new Company."""
        name = graphene.String(required=True, description="Company name")
        logo = Upload(required=False, description="Logo for the Company.",)


    def mutate(self, info: ResolveInfo, logo=None, **data) -> "CreateTestImage":
        """Mutate method."""
        file_data = {}
        if logo:
            file_data = {"logo": logo}

        # https://docs.djangoproject.com/en/3.2/ref/forms/api/#binding-uploaded-files-to-a-form
        # Binding file data to the Form.
        f = CreateTestImage.form(data, file_data)
 
        if f.is_valid():
            f.save()
            return CreateTestImage(success=True)
        else:
            return CreateTestImage(
                success=False, errors=f.errors.get_json_data()
            )


class CreateImageSerializer(graphene.Mutation, Output):

    class Arguments:
        """Necessary input to create a new Company."""
        name = graphene.String(required=True, description="Company name")
        logo = Upload(required=False, description="Logo for the Company.",)


    def mutate(self, info: ResolveInfo, logo=None, **data) -> "CreateImageSerializer":
        """Mutate method."""
        file_data = {}
        Print('logo', data)
        if logo:
            file_data = {"logo": logo}

        # https://docs.djangoproject.com/en/3.2/ref/forms/api/#binding-uploaded-files-to-a-form
        # Binding file data to the Form.
        data.update(file_data)
        serializer = TestForImageSerializer(data=data)
        # f = CreateImageSerializer.form(data, file_data)
 
        if serializer.is_valid():
            serializer.save()
            return CreateImageSerializer(success=True)
        else:
            return CreateImageSerializer(
                success=False, errors=serializer.errors
            )