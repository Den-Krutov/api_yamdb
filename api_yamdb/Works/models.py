from django.db import models


# Модель для приложений.
class Works(models.Model):
    name = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    titles_id = models.IntegerField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name

