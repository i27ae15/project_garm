# Generated by Django 4.1.4 on 2023-01-06 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_postcomment_deleted_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.CharField(default='post', max_length=50),
        ),
    ]
