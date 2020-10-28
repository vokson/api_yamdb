from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated

from category.models import Titles

from .models import Review
from .permissions import IsOwnerOrModeratorRoleOrAdminRole
from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        author = self.request.user

        if Review.objects.filter(title=title, author=author).count() > 0:
            raise ValidationError({'title': 'Author may have only one review for title'})

        serializer.save(author=author, title=title)

    def get_permissions(self):
        if self.action in ('partial_update', 'update', 'destroy',):
            permission_classes = [IsOwnerOrModeratorRoleOrAdminRole]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        get_object_or_404(Titles, pk=title_id)

        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)

        serializer.save(author=self.request.user, review=review)

    def get_permissions(self):
        if self.action in ('partial_update', 'update', 'destroy',):
            permission_classes = [IsOwnerOrModeratorRoleOrAdminRole]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
