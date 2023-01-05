from random import randint

from django.test import TestCase

from users.models import CustomUser as User, FriendRequest, UserInteraction, InteractionAction
from users.utils.enums import LinkedListTypeEnum, UserInteractionActionEnum

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

        self.possible_actions_with_score = [
            UserInteractionActionEnum.LIKE,
            UserInteractionActionEnum.COMMENT,
            UserInteractionActionEnum.TAG,
        ]

        return super().setUp()

    
    def ytest_create_interaction(self):

        self.assertEqual(check_if_friends(self.user_one, self.user_two), True)
        self.assertEqual(self.user_one.get_interactions().count(), 1)
        self.assertEqual(self.user_two.get_interactions().count(), 1)

        add_friends(self.user_one, num_friends=10)
        
        self.assertEqual(self.user_one.get_interactions().count(), 11)
        self.assertNotEqual(self.user_one.interaction_head_with_score, None)
        self.assertEqual(self.user_one.interactions_score, 55)

    
    def test_create_action_two_users(self):
            
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


        for _ in range(100):
            # get a random action
            action = self.possible_actions_with_score[randint(0, len(self.possible_actions_with_score)-1)]
            self.user_one.create_action(self.user_two, action)
            num_actions += 1
        
        self.assertEqual(interaction.get_actions().count(), num_actions)
        interaction.refresh_from_db()
        self.assertEqual(interaction.score < 100, True)
        # Print('score', interaction.score)


    def test_create_actions_between_multiple_users(self):
        # Perform a better test here
        add_friends(self.user_one, num_friends=10)
        
        self.assertEqual(self.user_one.get_interactions().count(), 11)
        self.assertNotEqual(self.user_one.interaction_head_with_score, None)
        self.assertEqual(self.user_one.interactions_score, 55)

        friends = self.user_one.friends.all()

        # gen = self.user_one.traverse_linked_list(LinkedListTypeEnum.WITH_SCORE)
        # while True:
        #     try:
        #         Print(next(gen).updated_at)
        #     except StopIteration:
        #         break

        Print('score head', self.user_one.interaction_head_with_score)
        Print('no score head', self.user_one.interaction_head_without_score)

        for _ in range(100):
            # get a random action
            action = self.possible_actions_with_score[randint(0, len(self.possible_actions_with_score)-1)]
            friend = friends[randint(0, len(friends)-1)]
            self.user_one.create_action(friend, action)
        self.user_one.refresh_from_db()
        Print('score', self.user_one.interactions_score)


