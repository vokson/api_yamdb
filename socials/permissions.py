from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class IsAdminOrIsModerator(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_admin_or_moderator = request.user.is_staff or request.user.role == 'moderator'
        return (view.action in ['update', 'partial_update', 'destroy']
                and is_admin_or_moderator)
