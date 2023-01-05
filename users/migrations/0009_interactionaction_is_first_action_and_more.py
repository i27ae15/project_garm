# Generated by Django 4.1.4 on 2023-01-03 00:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_userinteraction_is_blocked'),
    ]

    operations = [
        migrations.AddField(
            model_name='interactionaction',
            name='is_first_action',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='interactionaction',
            name='interaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interaction_actions', to='users.userinteraction'),
        ),
    ]