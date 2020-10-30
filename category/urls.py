from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from users.views import obtain_confirmation_code

from .views import CategoryViewSet, GenresViewSet, TitlesViewSet

v1_router = DefaultRouter()
v1_router.register('titles', TitlesViewSet, basename='titles')
v1_router.register('genres', GenresViewSet, basename='genres')
v1_router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
urlpatterns += [
    path('v1/auth/email/', obtain_confirmation_code,
         name='confirmation_token_obtain'),
    path('v1/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
]
