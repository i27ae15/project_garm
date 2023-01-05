from django.test import TestCase
from django.urls import reverse

from .utils import create_challenge, create_challenge_of_the_day, create_challenge_post

from print_pp.logging import Print

class TestChallengePost(TestCase):
    def setUp(self) -> None:
        self.challenge = create_challenge()[0]
        self.challenge_post = create_challenge_post(challenge=self.challenge)
        return super().setUp()

    def test_get_challenge_post(self):
        url = reverse('graphql')

        query = '''
            query {
                allChallengePost {
                    edges {
                        node {
                            owner {
                                username
                            }
                            challenge {
                                name
                            }
                        }
                    }
                }
            }
        '''
        response = self.client.post(url, {'query': query})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'data': {
                'allChallengePost': {
                    'edges': [
                        {
                            'node': {
                                'owner': {
                                    'username': self.challenge_post.owner.username
                                },
                                'challenge': {
                                    'name': self.challenge_post.challenge.name
                                }
                            }
                        }
                    ]
                }
            }
        })


    def test_challenge_post_create(self):
        create_challenge_of_the_day()
        url = reverse('graphql')

        query = '''
            mutation {
                createChallengePost(input: {owner: 2, description: "This is a test post"}) {
                    errors,
                    challengePost {
                        id
                        owner {
                            username
                        }
                        challenge {
                            name
                        }
                        description
                    }
                }
            }
        '''
        response = self.client.post(url, {'query': query})
        self.assertEqual(response.status_code, 200)


    def test_challenge_post_comment(self):
        url = reverse('graphql')

        query = '''
            mutation {
                createChallengePostComment(input: {owner: 2, challengePost: 1, comment: "This is a test comment"}) {
                    errors,
                    challengePostComment {
                        id
                        owner {
                            username
                        }
                        challengePost {
                            id
                        }
                        comment
                    }
                }
            }
        '''
        response = self.client.post(url, {'query': query})
        Print('new comment', response.json())
        self.assertEqual(response.status_code, 200)