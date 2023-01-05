from django.test import TestCase
from django.urls import reverse
from .models import CustomUser as User

from secrets import token_urlsafe
from print_pp.logging import Print

import random
from faker import Faker

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
        user.friends.add(friend)
        friends.append(friend)

    return friends


# test functions

def check_if_friends(user:User, user2:User):
    return user2 in user.friends.all() and user in user2.friends.all()


class TestGraphQL(TestCase):
    def setUp(self) -> None:
        self.user = create_user()[0]
        return super().setUp()

    def get_user(self):

        url = reverse('graphql')

        query = '''
            query {
                allUser {
                    edges {
                        node {
                            id
                            username
                        }
                    }
                }
            }
        '''
        response = self.client.post(url, {'query': query})
        Print('response', response.json())
    
    
    def send_friend_request(self):
        url = reverse('graphql')

        query = '''
            mutation {
                createFriendRequest(input: {fromUser: 1, toUser: 2}) {
                    errors,
                    friendRequest {
                        id
                        fromUser {
                            username
                        }
                        toUser {
                            username
                        }
                    }
                }
            }
        '''
        response = self.client.post(url, {'query': query})

        # create a function to create friend request
        url = reverse('graphql')

        query = '''
            mutation {
                acceptRejectFriendRequest(id: 1, accepted: true) {
                    deleted,
                    friendRequest {
                        id
                        fromUser {
                            username
                        }
                        toUser {
                            username
                        }
                    }
                }
            }
        '''
        response = self.client.post(url, {'query': query})
        Print('response', response.json())

    def accept_friend_request(self):
        url = reverse('graphql')

        query = '''
            mutation {
                acceptRejectFriendRequest(id: 1, accepted: true) {
                    deleted,
                    friendRequest {
                        id
                        fromUser {
                            username
                        }
                        toUser {
                            username
                        }
                    }
                }
            }
        '''
        response = self.client.post(url, {'query': query})
        Print('response', response.json())

    def get_user_friends(self):
        friends = add_friends(self.user, 10)
        for friend in friends:
            if not check_if_friends(self.user, friend):
                self.fail('No son amigos')

        url = reverse('graphql')

        query = '''
            query {
                allUser (id: 1) {
                    edges {
                        node {
                            id
                            username
                            friends {
                                edges {
                                    node {
                                        username
                                    }
                                }
                            }
                        }
                    }
                }
            }
        '''
        response = self.client.post(url, {'query': query})
        Print('response', response.json())


    def create_user(self):
        # Crea un usuario de prueba
        user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

        # Realiza una mutación de GraphQL para crear un nuevo usuario
        query = '''
            mutation {
                createUser(input: {username: "newuser", password: "newpass"}) {
                    user {
                        id
                        username
                    }
                }
            }
        '''
        response = self.client.post(
            reverse('graphql'),
            {'query': query},
            HTTP_AUTHORIZATION=f'JWT {user.auth_token.key}'
        )
        content = response.json()

        # Comprueba que la mutación haya sido exitosa y que el nuevo usuario tenga el nombre esperado
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['data']['createUser']['user']['username'], 'newuser')


    def test_get_user(self):
        # self.get_user()
        # self.get_user_friends()
        self.send_friend_request()
        # self.accept_friend_request()