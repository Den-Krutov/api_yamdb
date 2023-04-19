from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet, CommentViewSet, TitleViewSet, GenreViewSet, CategoriesViewSet

router_v1 = DefaultRouter()

routers_v1.register(r'titles', TitleViewSet, basename='titles'),
routers_v1.register(r'genre', GenreViewSet, basename='genre'),
routers_v1.register(r'categories', CategoriesViewSet, basename='categories'),
router_v1.register(
    'titles/(?P<title_id>\\d+)/reviews', ReviewViewSet, basename='reviews')
router_v1.register(
    'titles/(?P<title_id>\\d+)/reviews/(?P<review_id>\\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
