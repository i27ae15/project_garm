# Generated by Django 4.1.4 on 2023-01-06 03:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_interactionaction_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='race',
            name='specie',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.specie'),
        ),
    ]
