from challenges.models import Challenge, ChallengePost, ChallengePostComment, ChallengeOfTheDay
from user_info.models import CustomUser as User

from user_info.tests import create_user


def create_challenge(num_challenges=1):
    challenges = []

    for _ in range(num_challenges):
        challenge = Challenge.objects.create(
            name='Test Challenge' + str(_),
            description='This is a test challenge',
            image='challenges/images/test.jpg'
        )
        challenges.append(challenge)

    return challenges


def create_challenge_post(owner=None, challenge=None):
    owner = create_user()[0] if not owner else owner
    return ChallengePost.objects.create(
        owner=owner,
        challenge=challenge,
        description='This is a test challenge post'
    )


def create_challenge_of_the_day(challenge=None):
    challenge = create_challenge()[0] if not challenge else challenge
    return ChallengeOfTheDay.objects.create(
        challenge=challenge
    )


def create_challenge_post_comment(post:ChallengePost, owner=None):
    owner = create_user()[0] if not owner else owner
    return ChallengePostComment.objects.create(
        owner=owner,
        challenge_post=post,
        comment='This is a test comment'
    )