from django.contrib.auth import get_user_model
from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticatedOrReadOnly)

User = get_user_model()


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return User.ADMIN == request.user.role
        return False


class IsReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsAllowToView(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True

        return (
            request.user.is_staff or
            request.user.role in (User.MODERATOR, User.ADMIN,) or
            obj.author == request.user
        )
