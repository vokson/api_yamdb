from rest_framework.permissions import BasePermission, SAFE_METHODS

from loguru import logger


class IsReadOnly(BasePermission):
    def has_permission(self, request, view):
        logger.debug('IsReadOnly.has_permission')
        logger.debug(str(request.method in SAFE_METHODS))
        return request.method in SAFE_METHODS
