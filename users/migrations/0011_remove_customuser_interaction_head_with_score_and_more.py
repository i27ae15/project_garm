# Generated by Django 4.1.4 on 2023-01-03 02:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_userinteraction_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='interaction_head_with_score',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='interaction_head_without_score',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='interaction_tail_with_score',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='interaction_tail_without_score',
        ),
    ]
