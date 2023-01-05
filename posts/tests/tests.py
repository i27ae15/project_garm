from django.test import TestCase
from django.urls import reverse

from posts.tests.utils import create_posts
from users.tests.utils import create_user

from print_pp.logging import Print


class TestGraphQL(TestCase):
    def setUp(self) -> None:
        self.user = create_user()[0]
        return super().setUp()


    def get_posts(self):
        num_posts = 10
        create_posts(self.user, num_posts)
        url = reverse('graphql')
        query = '''
            query {
                allPost {
                    edges {
                        node {
                            id
                            description
                            image
                            comments {
                               edges {
                                    node {
                                        id
                                    }
                                }
                            }
                            author {
                                username
                            }
                        }
                    }
                }
            }
        '''
        response = self.client.post(url, {'query': query})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['data']['allPost']['edges']), num_posts)


    def create_posts_test(self):
        url = reverse('graphql')
        query = '''
            mutation {
                createPost(input: {
                    description: "This is a test post", image: "media/test_images/Screenshot_26.png", author: 1}) {
                    errors,
                    post {
                        id
                        description
                        image
                        author {
                            username
                        }
                    }
                }
            }
        '''
        response = self.client.post(url, {'query': query})
        Print('response', response.json())

    def test_get_posts(self):
        self.get_posts()
        self.create_posts_test()