from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model

from .models import MyUser

from loguru import logger


User = get_user_model()

# class IsOwnerOrReadOnly(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.method in SAFE_METHODS or obj == request.user


class IsMyself(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return obj == request.user
        return False


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return MyUser.ADMIN == request.user.role
        return False
