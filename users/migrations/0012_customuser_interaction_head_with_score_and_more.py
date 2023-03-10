# Generated by Django 4.1.4 on 2023-01-03 02:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_remove_customuser_interaction_head_with_score_and_more'),
    ]

    operations = [
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
