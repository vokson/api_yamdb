from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, obtain_auth_token, obtain_confirmation_code

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)

urlpatterns = [
    path('v1/auth/email/', obtain_confirmation_code, name='confirmation_token_obtain'),
    path('v1/auth/token/', obtain_auth_token, name='token_obtain_pair'),
    path('v1/', include(router_v1.urls)),
]
