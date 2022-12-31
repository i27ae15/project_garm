from django.test import TestCase

from users.models import CustomUser as User, FriendRequest, UserInteraction, InteractionAction
from users.utils.enums import UserInteractionActionEnum

from .utils import create_user, add_friends, check_if_friends


def traverse_linked_list(node:UserInteraction):
    while node:
        print(node)
        node = node.next_node


class TestCreateInteraction(TestCase):

    def setUp(self) -> None:

        users = create_user(n=2)
        self.user_one = users[0]
        self.user_two = users[1]

        return super().setUp()

    
    def test_create_interaction(self):

        self.user_one.add_friend(self.user_two)

        self.assertEqual(check_if_friends(self.user_one, self.user_two), True)
        self.assertEqual(self.user_one.get_interactions().count(), 1)
        self.assertEqual(self.user_two.get_interactions().count(), 1)

        add_friends(self.user_one, num_friends=10)
        
        self.assertEqual(self.user_one.get_interactions().count(), 11)
        self.assertNotEqual(self.user_one.interaction_head_with_score, None)

        traverse_linked_list(self.user_one.interaction_head_with_score)


