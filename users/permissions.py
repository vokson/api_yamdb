from django.contrib.auth import get_user_model
from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

User = get_user_model()


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return User.ADMIN == request.user.role
        return False


class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsAuthorOrReadOnly(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdminOrIsModerator(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        is_admin_or_moderator = request.user.is_staff or request.user.role == 'moderator'
        return (view.action in ['update', 'partial_update', 'destroy']
                and is_admin_or_moderator)


class IsAllowToView(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return view.action not in ['create', 'update', 'partial_update', 'destroy']
