from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

from .models import MyUser

User = get_user_model()


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return MyUser.ADMIN == request.user.role
        return False
