from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.views import obtain_confirmation_code, obtain_auth_token
from .views import CategoryViewSet, GenresViewSet, TitlesViewSet


v1_router = DefaultRouter()
v1_router.register('titles', TitlesViewSet, basename='titles')
v1_router.register('genres', GenresViewSet, basename='genres')
v1_router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
