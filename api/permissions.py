from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from .models import User


class IsAdminRole(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_admin


class IsReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsAllowToView(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True

        return (
            request.user.is_admin or
            request.user.is_moderator or
            obj.author == request.user
        )
