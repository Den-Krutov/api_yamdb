from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Title(models.Model):
    rating = models.IntegerField(
        verbose_name='Рейтинг (средняя оценка)',
        null=True,
        default=None
    )


class Review(models.Model):
    score = models.IntegerField(
        verbose_name='Оценка произведения',
        validators=[
            MinValueValidator(1, 'Выберите оценку от 1 до 10'),
            MaxValueValidator(10, 'Выберите оценку от 1 до 10')
        ]
    )
