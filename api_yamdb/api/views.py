from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import viewsets, mixins, filters, status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    UserSerializer, TokenSerializer, TitleSerializer, GenreSerializer,
    CategoriesSerializer, ReviewSerializer, CommentSerializer)
from reviews.models import User, Title, Genre, Categories, Review
from .utils import send_confirm_code


class SignUpView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        user = self.queryset.filter(username=username, email=email).first()
        if user:
            send_confirm_code(user)
            return Response(data=request.data, status=status.HTTP_200_OK)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_confirm_code(serializer.instance)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(GenericAPIView):
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(
                data=serializer.validated_data, status=status.HTTP_200_OK)
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'year', 'name')


class CategoriesViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    pagination_class = None
    search_fields = ('name',)


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Review."""
    serializer_class = ReviewSerializer
    permission_classes = []

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = []

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class TitleViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Title.objects.annotate(rating=Avg('reviews__score'))
