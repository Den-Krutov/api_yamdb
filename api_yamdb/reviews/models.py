from django.contrib.auth import base_user, validators
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

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

    def __str__(self) -> str:
        return self.username

    def is_admin(self):
        return self.role == ROLES[2][0] or self.is_staff

    def is_moderator(self):
        return self.role == ROLES[1][0]


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)
    description = models.CharField(max_length=256, required=False)
    rating = models.IntegerField(
        verbose_name='Рейтинг (средняя оценка)',
        null=True,
        default=None
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзыва на произведение."""
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        max_length=1000
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка произведения',
        validators=[
            MinValueValidator(1, 'Оценка не может быть меньше 1!'),
            MaxValueValidator(10, 'Оценка не может быть больше 10!')
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации отзыва',
        auto_now_add=True
    )

    class Meta:
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]

    def __str__(self) -> str:
        return self.text[:15]


class Comment(models.Model):
    """Модель комментария на отзыв."""
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        max_length=500
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации комментария',
        auto_now_add=True
    )

    class Meta:
        ordering = ['pub_date']

    def __str__(self) -> str:
        return self.text[:15]
