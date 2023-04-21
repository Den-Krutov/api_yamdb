from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator as dtg
from rest_framework import serializers, validators
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken


from reviews.models import (
    User, Title, Genre, Categories, Review, Title, Comment)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username']


class TokenSerializer(TokenObtainSerializer):
    token_class = AccessToken

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')
        self.fields['confirmation_code'] = serializers.CharField()

    def validate(self, attrs):
        return {'token': str(self.get_token(self.user))}

    def validate_username(self, username):
        self.user = get_object_or_404(User, username=username)
        return username

    def validate_confirmation_code(self, confirmation_code):
        if not dtg.check_token(self.user, confirmation_code):
            raise serializers.ValidationError('Неверный confirmation_code')
        return confirmation_code


class TitleSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(
        slug_field='name', read_only=True)
    genre = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(
        slug_field='name', read_only=True)
    title = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Genre
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(slug_field='name', read_only=True)
    genre = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Categories
        fields = '__all__'


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
