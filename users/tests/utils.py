import random

from faker import Faker
from secrets import token_urlsafe
from users.models import CustomUser as User

Faker.seed(115)
fake = Faker()


def create_user(own_data:dict = None, n = 10) -> list[User]:

    if own_data:
        user_object = User.objects.create_user(**own_data)
        return [user_object]

    users = []
    for _ in range(n):
        user = {
            'email': fake.email(),
            'education': random.choice(['B', 'M', 'D', 'P', 'N']),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'phone': fake.phone_number(),
            'username': fake.user_name(),
            'sex': random.choice(['M', 'F']),
            'job': fake.job(),
            'password': token_urlsafe(),
        }
        user_object = User.objects.create_user(**user)
        users.append(user_object)

    return users


def add_friends(user:User, num_friends=10) -> list[User]:
    friends = []
    
    for _ in range(num_friends):
        friend = create_user(n=1)[0]
        user.add_friend(friend)
        friends.append(friend)

    return friends


def check_if_friends(user:User, user2:User):
    return user2 in user.friends.all() and user in user2.friends.all()
