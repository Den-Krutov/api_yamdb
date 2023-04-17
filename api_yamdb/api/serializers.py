from django.shortcuts import get_object_or_404
from rest_framework import serializers, validators

from reviews.models import Review, Title, Comment


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'

    validators = [
        validators.UniqueTogetherValidator(
            queryset=Review.objects.all(),
            fields=['title', 'author'],
        )
    ]

    def validate(self, data):
        """Проверяем, что пользователь не может оставить второй отзыв."""
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        author = self.context['request'].user
        if (
            self.context['request'].method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на данное произведение.')
        return data

    def validate_score(self, value):
        """Проверяем, что оценка соответствует шкале от 1 до 10."""
        if not 1 <= value <= 10:
            raise serializers.ValidationError('Допустимый диапазон оценки:'
                                              'от 1 до 10')
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.SlugRelatedField(
        read_only=True,
        slug_field='text'
    )

    class Meta:
        model = Comment


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'
