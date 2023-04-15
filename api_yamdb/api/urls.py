from django.urls import path, include
from .views import TitleViewSet, GenreViewSet, CategoriesViewSet
from rest_framework import routers

routers_v1 = routers.SimpleRouter()
routers_v1.register(r'titles', TitleViewSet, basename='titles'),

routers_v2 = routers.SimpleRouter()
routers_v2.register(r'genre', GenreViewSet, basename='genre'),

routers_v3 = routers.SimpleRouter()
routers_v3.register(r'categories', CategoriesViewSet, basename='categories'),

urlpatterns = [
    path('v1/', include(routers_v1.urls)),
    path('v2/', include(routers_v2.urls)),
    path('v3/', include(routers_v3.urls)),
]
