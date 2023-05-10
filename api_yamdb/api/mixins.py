from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (mixins, viewsets)
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from api.permissions import AdminOrReadOnly


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    permission_classes = [AdminOrReadOnly]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    pagination_class = PageNumberPagination
    search_fields = ['name']
    lookup_field = 'slug'
