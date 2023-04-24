from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    filters, mixins, permissions, status, viewsets, decorators)
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from reviews.models import Categories, Genre, Review, Title, User
from .permissions import Admin, AdminOrReadOnly, Moderator
from .serializers import (CategoriesSerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          TokenSerializer, SignUpSerializer, UserSerializer,
                          AdminUserSerializer)
from .utils import send_confirm_code


class SignUpView(GenericAPIView):
    """Класс регистрации новых пользователей"""

    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(
            **serializer.validated_data
        )
        send_confirm_code(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class TokenView(GenericAPIView):
    """Получение токена с помощью username пользователя и confirmation_code"""

    serializer_class = TokenSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(
                data=serializer.validated_data, status=status.HTTP_200_OK)
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = AdminUserSerializer
    permission_classes = (Admin,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return User.objects.order_by('username')

    @decorators.action(
        detail=False, methods=['get', 'patch'], url_name='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        serializer = self.serializer_class(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin():
                serializer = self.serializer_class(
                    request.user, data=request.data, partial=True)
            else:
                serializer = UserSerializer(
                    request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [AdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'year', 'name')

    def get_queryset(self):
        return Title.objects.annotate(Avg('reviews__score'))


class CategoriesViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [AdminOrReadOnly]


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AdminOrReadOnly]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    pagination_class = None
    search_fields = ('name',)


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Review."""
    serializer_class = ReviewSerializer
    permission_classes = [Moderator]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = [Moderator]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
