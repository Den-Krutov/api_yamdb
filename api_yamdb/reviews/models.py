from django.db import models


# Модель для приложений.
class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.name


# Модель для категорий.
class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.name


# Модель для произведений.
class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    categories = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=256)

    def __str__(self):
        return self.name


