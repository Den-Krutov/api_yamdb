from rest_framework import generics
from api_yamdb.reviews.models import Title
from api_yamdb.api.serializers import WorkSerializer


# Выполняем проверку по slug.
class TitleList(generics.ListAPIView):
    serializer_class = WorkSerializer

    def get_queryset(self):
        queryset = Title.objects.all()
        category_slug = self.request.query_params.get('category', None)
        if category_slug is not None:
            queryset = queryset.filter(category__slug=category_slug)
        genre_slug = self.request.query_params.get('genre', None)
        if genre_slug is not None:
            queryset = queryset.filter(genre__slug=genre_slug)
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        year = self.request.query_params.get('year', None)
        if year is not None:
            queryset = queryset.filter(year=year)
        return queryset
