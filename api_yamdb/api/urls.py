from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SignUpView

router_v1 = DefaultRouter()

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
]
