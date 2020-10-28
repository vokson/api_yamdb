from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

User = get_user_model()

from loguru import logger

class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        logger.debug('IsAdminRole.has_permission')
        if request.user.is_authenticated:
            logger.debug(str(User.ADMIN == request.user.role))
            return User.ADMIN == request.user.role
        return False
