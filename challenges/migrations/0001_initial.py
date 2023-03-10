# Generated by Django 4.1.4 on 2022-12-29 17:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('image', models.ImageField(null=True, upload_to='challenges/images')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChallengePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='challenges/posts')),
                ('created_at', models.DateTimeField()),
                ('description', models.TextField(default='')),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='challenge_post', to='challenges.challenge')),
                ('likes', models.ManyToManyField(blank=True, related_name='challenge_posts_likes', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='challenge_post_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChallengePostComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField()),
                ('challenge_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='challenges.challengepost')),
                ('likes', models.ManyToManyField(blank=True, related_name='challenge_post_comments_likes', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='challenge_post_comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChallengeOfTheDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='challenge_of_the_day', to='challenges.challenge')),
                ('challenge_post_winner', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='challenge_of_the_day', to='challenges.challengepost')),
            ],
        ),
    ]
