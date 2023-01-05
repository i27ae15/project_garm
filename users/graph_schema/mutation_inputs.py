import graphene


class FriendRequestInput(graphene.InputObjectType):
    from_user = graphene.Int() # I guess this can be gotten from the token, but I'm not sure
    to_user = graphene.Int()


