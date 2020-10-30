from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


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
