from posts.models import Post

from users.models import CustomUser as User
from users.tests.utils import create_user

from faker import Faker
from secrets import token_urlsafe

Faker.seed(115)
fake = Faker()

def create_posts(owner:User, num=10) -> list[Post]:
    posts = []
    for _ in range(num):
        post = {
            'description': fake.sentence(),
            'author': owner,
            'image': f'media/test_images/Screenshot_26.png'
        }
        post_object = Post.objects.create(**post)
        posts.append(post_object)
    return posts
