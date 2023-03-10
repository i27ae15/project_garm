# Generated by Django 4.1.4 on 2022-12-31 07:37

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0001_initial'),
        ('users', '0003_testforimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='posts_seen_in_last_24_hours',
        ),
        migrations.AddField(
            model_name='customuser',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='profile_photos'),
        ),
        migrations.CreateModel(
            name='UserInteraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(30)])),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('comments', models.TextField(blank=True, null=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interactions_sent', to=settings.AUTH_USER_MODEL)),
                ('next_node', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_interaction_node', to='users.userinteraction')),
                ('previous_node', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='previous_interaction_node', to='users.userinteraction')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interactions_received', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InteractionAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.IntegerField(choices=[(1, 'Follow'), (2, 'Unfollow'), (3, 'Block'), (4, 'Unblock'), (5, 'Report'), (6, 'Unreport'), (7, 'Like'), (8, 'Unlike'), (9, 'Add Friend'), (10, 'Remove Friend'), (11, 'Comment'), (12, 'Answer Comment'), (13, 'Tag')], default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('challenge_post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='challenges.challengepost')),
                ('interaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions', to='users.userinteraction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='interaction_head_with_score',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interaction_head_with_score', to='users.userinteraction'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='interaction_head_without_score',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interaction_head_without_score', to='users.userinteraction'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='interaction_tail_with_score',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interaction_tail_with_score', to='users.userinteraction'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='interaction_tail_without_score',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interaction_tail_without_score', to='users.userinteraction'),
        ),
    ]
