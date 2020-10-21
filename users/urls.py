from django.urls import include, path
# from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    # TokenRefreshView
    TokenViewBase
)
from rest_framework_simplejwt.serializers import serializers

from .views import obtain_auth_token

# from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        kwargs['data']['password'] = kwargs['data'].get('confirmation_code', '')

        if not kwargs['data']['password']:
            raise serializers.ValidationError({'confimation_code': ['This field may not be blank.']})

        super().__init__(*args, **kwargs)


class CustomTokenObtainPairView(TokenViewBase):
    serializer_class = CustomTokenObtainPairSerializer

# router_v1 = DefaultRouter()
# router_v1.register('group', GroupViewSet, 'group')
# router_v1.register('follow', FollowViewSet, 'follow')
# router_v1.register('posts', PostViewSet, 'post')
# router_v1.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet, 'comment')


urlpatterns = [
    path('v1/auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/auth/get_token/', obtain_auth_token)
    # path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('v1/', include(router_v1.urls)),
]
