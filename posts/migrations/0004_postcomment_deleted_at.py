# Generated by Django 4.1.4 on 2023-01-05 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_rename_owner_postcomment_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomment',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
