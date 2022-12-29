# Generated by Django 4.1.4 on 2022-12-29 10:02

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Specie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('education', models.CharField(blank=True, max_length=255, null=True)),
                ('first_name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_tester', models.BooleanField(default=False)),
                ('is_email_confirmed', models.BooleanField(default=False)),
                ('last_name', models.CharField(max_length=255)),
                ('phone', models.CharField(default='', max_length=120)),
                ('registration_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('sex', models.CharField(default=None, max_length=1, null=True)),
                ('code_to_confirm_email', models.CharField(max_length=126, null=True)),
                ('job', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('posts_seen_in_last_24_hours', models.JSONField(default=list)),
                ('followers', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('following', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('friends', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('race', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.race')),
                ('specie', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.specie')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
