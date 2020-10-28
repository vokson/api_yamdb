from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

User = get_user_model()


from loguru import logger



class IsOwnerOrModeratorRoleOrAdminRole(BasePermission):
    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        logger.debug('IsOwnerOrModeratorRoleOrAdminRole.has_object_permission')
        logger.debug(obj.author)
        logger.debug(request.user)

        if request.user.is_authenticated:
            if User.MODERATOR == request.user.role or User.ADMIN == request.user.role:
                return True

        logger.debug(str(obj.author == request.user))
        return obj.author == request.user



class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        logger.debug('IsOwner.has_object_permission')
        logger.debug(obj.author)
        logger.debug(request.user)
        logger.debug(str(obj.author == request.user))
        return obj.author == request.user


class IsModeratorRole(BasePermission):
    def has_permission(self, request, view):
        logger.debug('IsModeratorRole.has_permission')
        if request.user.is_authenticated:
            logger.debug(str(User.MODERATOR == request.user.role))
            return User.MODERATOR == request.user.role
        return False
