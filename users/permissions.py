from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

User = get_user_model()


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return User.ADMIN == request.user.role
        return False
