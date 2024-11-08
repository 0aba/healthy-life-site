# Generated by Django 5.1.2 on 2024-11-06 19:04

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Awards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='award/%Y/%m/%d/', verbose_name='Изображение награды')),
                ('description', models.TextField(max_length=512, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Награда',
                'verbose_name_plural': 'Награды',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', models.ImageField(default='default/avatar.png', upload_to='users/avatars/%Y/%m/%d/', verbose_name='Аватарка')),
                ('background', models.ImageField(default='default/background.png', upload_to='users/backgrounds/%Y/%m/%d/', verbose_name='Задний фон')),
                ('about', models.TextField(blank=True, max_length=512, verbose_name='О себе')),
                ('last_seen', models.DateTimeField(auto_now=True)),
                ('is_online', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AwardsUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_awarded', models.DateTimeField(auto_now_add=True, verbose_name='Время награждения')),
                ('award', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='award_fk', to='user.awards', verbose_name='Награда')),
                ('award_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='award_user_fk', to=settings.AUTH_USER_MODEL, verbose_name='Изображение награды')),
            ],
            options={
                'verbose_name': 'Награда пользователя',
                'verbose_name_plural': 'Награды пользователей',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_subscribed_in_priority', models.BooleanField(default=True, verbose_name='Отображать контент подписок в приоритете')),
                ('display_bloggers_in_blacklisted', models.BooleanField(default=False, verbose_name='Не отображать контент от тех, кто а ЧС')),
                ('hide_yourself_subscriptions', models.BooleanField(default=False, verbose_name='Скрыть подписки')),
                ('receive_notifications_about_responses_messages', models.BooleanField(default=False, verbose_name='Получать уведмление об ответах на сооющения')),
                ('receive_notifications_about_discounts', models.BooleanField(default=False, verbose_name='Получать уведомления об скидках')),
                ('duplicate_notifications_to_email', models.BooleanField(default=False, verbose_name='Дублировать уведомления на почту')),
                ('user_settings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Настройки',
                'verbose_name_plural': 'Настройки',
            },
        ),
        migrations.CreateModel(
            name='BlackList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_black_list', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='in_black_list_fk', to=settings.AUTH_USER_MODEL)),
                ('user_black_list', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_black_list_fk', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ЧС',
                'verbose_name_plural': 'ЧС',
                'unique_together': {('user_black_list', 'in_black_list')},
            },
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friends_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='friends_user_fk', to=settings.AUTH_USER_MODEL)),
                ('user_friend', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_friend_fk', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Друг',
                'verbose_name_plural': 'Друзья',
                'unique_together': {('friends_user', 'user_friend')},
            },
        ),
    ]
