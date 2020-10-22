from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import obtain_auth_token, obtain_confirmation_code
from .views import MyUserViewSet, UserViewSet

# class App1Router(SimpleRouter):

#     routes = [
#         Route(
#             url = r'^{prefix}{trailing_slash}$',
#             mapping = {
#                 'get': 'retrieve',
#                 'post': 'create',
#                 'patch': 'partial_update',
#             },
#             name = '{basename}-user',
#             initkwargs = {}
#         ),
#     ]

router_v1 = DefaultRouter()
# router_v1.register('users', MyUserViewSet)
router_v1.register('users', UserViewSet)
# router_v1.register('follow', FollowViewSet, 'follow')
# router_v1.register('posts', PostViewSet, 'post')
# router_v1.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet, 'comment')


urlpatterns = [
    path('v1/auth/email/', obtain_confirmation_code, name='confirmation_token_obtain'),
    path('v1/auth/token/', obtain_auth_token, name='token_obtain_pair'),
    path('v1/', include(router_v1.urls)),
]
