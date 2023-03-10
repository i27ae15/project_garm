# Generated by Django 4.1.4 on 2023-01-05 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_customuser_interaction_head_with_score_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interactionaction',
            name='action',
            field=models.IntegerField(choices=[(1, 'Follow'), (2, 'Unfollow'), (3, 'Block'), (4, 'Unblock'), (5, 'Report'), (6, 'Unreport'), (7, 'Like'), (8, 'Unlike'), (9, 'Friendship'), (10, 'Unfriendship'), (11, 'Comment'), (12, 'Answer Comment'), (13, 'Delete Comment'), (14, 'Tag'), (15, 'Share')], default=0),
        ),
    ]
