from django.test import TestCase

from users.tests.utils import create_user
from .utils import (create_challenge, create_challenge_post, 
create_challenge_of_the_day, create_challenge_post_comment)

# Create your tests here.

class TestChallenge(TestCase):
    def setUp(self) -> None:
        self.user = create_user()[0]
        self.challenge = create_challenge()[0]
        self.challenge_post = create_challenge_post(self.user, self.challenge)
        self.challenge_of_the_day = create_challenge_of_the_day(self.challenge)
        self.challenge_post_comment = create_challenge_post_comment(self.challenge_post, self.user)
        return super().setUp()


    def test_challenge_post(self):
        self.assertEqual(self.challenge_post.owner, self.user)
        self.assertEqual(self.challenge_post.challenge, self.challenge)


    def test_challenge_of_the_day(self):
        self.assertEqual(self.challenge_of_the_day.challenge, self.challenge)


    def test_challenge_post_comment(self):
        self.assertEqual(self.challenge_post_comment.owner, self.user)
        self.assertEqual(self.challenge_post_comment.challenge_post, self.challenge_post)
        self.assertEqual(self.challenge_post_comment.comment, 'This is a test comment')


    def test_challenge_post_num_likes(self):
        self.assertEqual(self.challenge_post.num_likes, 0)


    def test_challenge_post_like(self):
        self.challenge_post.likes.add(self.user)
        self.assertEqual(self.challenge_post.num_likes, 1)


    def test_challenge_post_unlike(self):
        self.challenge_post.likes.add(self.user)
        self.assertEqual(self.challenge_post.num_likes, 1)
        self.challenge_post.likes.remove(self.user)
        self.assertEqual(self.challenge_post.num_likes, 0)


    def test_challenge_post_like_twice(self):
        self.challenge_post.likes.add(self.user)
        self.assertEqual(self.challenge_post.num_likes, 1)
        self.challenge_post.likes.add(self.user)
        self.assertEqual(self.challenge_post.num_likes, 1)


    def test_challenge_post_unlike_twice(self):
        self.challenge_post.likes.add(self.user)
        self.assertEqual(self.challenge_post.num_likes, 1)
        self.challenge_post.likes.remove(self.user)
        self.assertEqual(self.challenge_post.num_likes, 0)
        self.challenge_post.likes.remove(self.user)
        self.assertEqual(self.challenge_post.num_likes, 0)


    def test_challenge_post_like_and_unlike(self):
        self.challenge_post.likes.add(self.user)
        self.assertEqual(self.challenge_post.num_likes, 1)
        self.challenge_post.likes.remove(self.user)