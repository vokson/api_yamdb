from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_list_or_404

from category.permissions import IsReadOnly
from category.models import Titles
from .serializers import ReviewSerializer
from .models import Review, Comment
from .permissions import IsOwner, IsModeratorRole, IsOwnerOrModeratorRoleOrAdminRole
from users.permissions import IsAdminRole

from loguru import logger


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReadOnly | IsOwnerOrModeratorRoleOrAdminRole]
    # filterset_fields = ['username']
    # lookup_field = 'username'

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        logger.debug('ReviewViewSet.perform_create')
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        author = self.request.user

        # logger.debug('ReviewViewSet.perform_create')
        # logger.debug(title)

        if Review.objects.filter(title=title, author=author).count() > 0:
            raise ValidationError('Author may have only one review for title')

        serializer.save(author=author, title=title)

    # def perform_update(self, serializer):
    #     logger.debug('ReviewViewSet.perform_update')
    #     pass
