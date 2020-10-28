from django.urls import path, include
from rest_framework.routers import DefaultRouter

# from socials.views import ReviewView, CommentView
from socials.views import ReviewViewSet

v1_router = DefaultRouter()
v1_router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
# v1_router.register(r'title/(?P<title_id>\d+)/reviews', ReviewView, basename='reviews')
# v1_router.register(r'title/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentView, basename='comments')

urlpatterns = [
    path('v1/', include(v1_router.urls))
]
