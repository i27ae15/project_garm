from random import randint

from django.test import TestCase

from users.models import CustomUser as User, FriendRequest, UserInteraction, InteractionAction
from users.utils.enums import UserInteractionActionEnum

from .utils import create_user, add_friends, check_if_friends

from print_pp.logging import Print


def traverse_linked_list(node:UserInteraction):
    while node:
        print(node)
        node = node.next_node


class TestCreateInteraction(TestCase):

    def setUp(self) -> None:

        users = create_user(n=2)
        self.user_one = users[0]
        self.user_two = users[1]
        self.user_one.add_friend(self.user_two)

        Print('after being friends')

        return super().setUp()

    
    def ytest_create_interaction(self):

        self.assertEqual(check_if_friends(self.user_one, self.user_two), True)
        self.assertEqual(self.user_one.get_interactions().count(), 1)
        self.assertEqual(self.user_two.get_interactions().count(), 1)

        add_friends(self.user_one, num_friends=10)
        
        self.assertEqual(self.user_one.get_interactions().count(), 11)
        self.assertNotEqual(self.user_one.interaction_head_with_score, None)
        self.assertEqual(self.user_one.interactions_score, 55)

        # traverse_linked_list(self.user_one.interaction_head_with_score)

    
    def test_create_action(self):
            
        self.assertEqual(self.user_one.get_interactions().count(), 1)
        self.assertEqual(self.user_two.get_interactions().count(), 1)

        interaction:UserInteraction = self.user_one.get_interactions(user_id=self.user_two.pk).first()
        num_actions = 1

        # this should produce an error
        error = None
        try:
            self.user_one.create_action(self.user_two, UserInteractionActionEnum.FRIENDSHIP)
        except Exception as e:
            error = e
        self.assertNotEqual(error, None)
        self.assertEqual(interaction.get_actions().count(), 1)

        error = None
        try:
            self.user_one.create_action(self.user_two, UserInteractionActionEnum.FOLLOW)
        except Exception as e:
            error = e
        self.assertNotEqual(error, None)
        self.assertEqual(interaction.get_actions().count(), 1)
        

        possible_actions_with_score = [
            UserInteractionActionEnum.LIKE,
            UserInteractionActionEnum.COMMENT,
            UserInteractionActionEnum.TAG,
        ]

        for _ in range(10):
            # get a random action
            action = possible_actions_with_score[randint(0, len(possible_actions_with_score)-1)]
            self.user_one.create_action(self.user_two, action)
            num_actions += 1
        
        self.assertEqual(interaction.get_actions().count(), num_actions)
        Print(('after creating actions'), ('actions', interaction.get_actions()))
        interaction.refresh_from_db()
        Print('score', interaction.score)
