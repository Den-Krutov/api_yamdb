from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ReviewViewSet, CommentViewSet, TitleViewSet, GenreViewSet,
    CategoriesViewSet, SignUpView)

router_v1 = DefaultRouter()

router_v1.register(r'titles', TitleViewSet, basename='titles'),
router_v1.register(r'genre', GenreViewSet, basename='genre'),
router_v1.register(r'categories', CategoriesViewSet, basename='categories'),
router_v1.register(
    'titles/(?P<title_id>\\d+)/reviews', ReviewViewSet, basename='reviews')
router_v1.register(
    'titles/(?P<title_id>\\d+)/reviews/(?P<review_id>\\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
]
