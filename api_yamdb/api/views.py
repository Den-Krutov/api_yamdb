from django.contrib.auth.models import Permission
from rest_framework import viewsets
from rest_framework.decorators import permission_classes

from reviews.models import Title, Genre, Categories
from api.serializers import TitleSerializer, GenreSerializer, CategoriesSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework import filters


# Вьюсет для произведений.
class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'year', 'name')


# Вьюсет для категорий.
class CategoriesViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        GenericViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


# Вьюсет для жанров.
class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    pagination_class = None
    search_fields = ('name',)
