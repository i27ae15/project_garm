# Generated by Django 4.1.4 on 2023-01-03 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_rename_user_interactionaction_made_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinteraction',
            name='are_friends',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userinteraction',
            name='is_following',
            field=models.BooleanField(default=False),
        ),
    ]