from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


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


class User(AbstractUser):
    email = models.EmailField('email адрес', unique=True)
