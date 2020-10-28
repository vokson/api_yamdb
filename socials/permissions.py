from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

User = get_user_model()


class IsOwnerOrModeratorRoleOrAdminRole(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if User.MODERATOR == request.user.role or User.ADMIN == request.user.role:
                return True

        return obj.author == request.user
