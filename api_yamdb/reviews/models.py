from django.contrib.auth import base_user, validators
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import no_me_username_validator

ROLES = [
    ('user', 'пользователь'), ('moderator', 'модератор'),
    ('admin', 'администратор')]
DEFAULT_USER_ROLE = ROLES[0][0]


class UserManager(base_user.BaseUserManager):
    def create_user(self, username, email):
        if not email:
            raise ValueError('Введите email')
        if not username:
            raise ValueError('Введите никнейм пользователя')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_unusable_password()
        user.save()
        return user


class User(AbstractUser):
    username_validator = validators.UnicodeUsernameValidator()

    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text='Введите уникальный username пользователя',
        validators=[username_validator, no_me_username_validator],
        error_messages={
            'unique': "Пользователь с таким именем уже существует",
        },
    )
    email = models.EmailField(
        'email адрес', max_length=254, unique=True,
        help_text='Введите email адрес')
    bio = models.TextField(
        'Биография', blank=True, help_text='Введите биографию пользователя')
    role = models.CharField(
        'Роль', max_length=64, choices=ROLES, default=DEFAULT_USER_ROLE,
        help_text='Выберите роль пользователя')

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username='me'),
                name='no_username_me',
            ),
        ]
