from rest_framework import serializers
from .models import Works


# Сериализатор для произведений.
class WorkSerializer(serializers.ModelSerializer):
    Category = serializers.StringRelatedField()
    Genre = serializers.StringRelatedField()

    class Meta:
        model = Works
        fields = ('id', 'name', 'year', 'category', 'genre', 'description', 'titles_id')
