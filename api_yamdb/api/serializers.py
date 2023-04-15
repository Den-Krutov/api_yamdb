from rest_framework import serializers
from reviews.models import Title, Genre, Categories


# Сериализатор для произведений.
class TitleSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(slug_field='name', read_only=True)
    genre = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


# Сериализатор для жанров.
class GenreSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(slug_field='name', read_only=True)
    title = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Genre
        fields = '__all__'


# Сериализатор для категорий.
class CategoriesSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(slug_field='name', read_only=True)
    genre = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Categories
        fields = '__all__'
