import django_filters
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator as dtg
from rest_framework import serializers, validators
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import (
    User, Genre, Category, Review, Title, Comment)


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.SlugField(max_length=150)

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError('username не может быть me')
        return username

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        user = User.objects.filter(username=username).first()
        if user and user.email != email:
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует')
        user = User.objects.filter(email=email).first()
        if user and user.username != username:
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует')
        return data


class TokenSerializer(TokenObtainSerializer):
    token_class = AccessToken

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')
        self.fields['confirmation_code'] = serializers.CharField()
        self.user = None

    def validate(self, data):
        return {'token': str(self.get_token(self.user))}

    def validate_username(self, username):
        self.user = get_object_or_404(User, username=username)
        return username

    def validate_confirmation_code(self, confirmation_code):
        if not self.user or not dtg.check_token(self.user, confirmation_code):
            raise serializers.ValidationError('Неверный confirmation_code')
        return confirmation_code


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio']


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'bio', 'role']


class TitleSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(
        slug_field='name', read_only=True)
    genre = serializers.SlugRelatedField(slug_field='name', read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']


class GenreSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(
        slug_field='name', read_only=True)
    title = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Genre
        fields = ['id', 'name', 'categories', 'title']


class CategorySerializer(serializers.ModelSerializer):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ['name']


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
