from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.views import obtain_confirmation_code, obtain_auth_token
from .views import CategoryViewSet, GenresViewSet, TitlesViewSet

# router = DefaultRouter()
# router.register()
# # router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='Comment')
# router.register('genres', GenresViewSet),
# router.register('categories', CategoryViewSet),

# urlpatterns = [
#     path('v1/', include(router.urls)),
# ]

# urlpatterns += [
#     path('v1/token/', TokenObtainPairView.as_view(),
#          name='token_obtain_pair'),
#     path('v1/token/refresh/', TokenRefreshView.as_view(),
#          name='token_refresh'),
# ]
router = DefaultRouter()
router.register('titles', TitlesViewSet)
router.register('genres', GenresViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
urlpatterns += [
    path('v1/auth/email/', obtain_confirmation_code, name='confirmation_token_obtain'),
    path('v1/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
]