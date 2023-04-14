from rest_framework import viewsets
from django.db.models import Avg

from reviews.models import Title


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
