from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

ROLES = [
    ('user', 'пользователь'), ('moderator', 'модератор'),
    ('admin', 'администратор')]
DEFAULT_USER_ROLE = ROLES[0][0]
DEFAULT_ADMIN_ROLE = ROLES[2][0]


class UserManager(BaseUserManager):
    def create_user(self, username, email):
        if not email:
            raise ValueError('Введите email')
        if not username:
            raise ValueError('Введите никнейм пользователя')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, username, email, **extra_fields):
        extra_fields.setdefault('role', DEFAULT_ADMIN_ROLE)
        return super().create_superuser(self, username, email, **extra_fields)


class User(AbstractUser):
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
