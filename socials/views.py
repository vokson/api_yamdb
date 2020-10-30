from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from category.models import Titles
from socials.models import Review
from socials.permissions import IsAuthorOrReadOnly, IsAdminOrIsModerator, IsAllowToView
from socials.serializers import ReviewSerializer, CommentSerializer


class ReviewView(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly | IsAdminOrIsModerator | IsAllowToView]

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        author = self.request.user

        if Review.objects.filter(title=title, author=author).count() > 0:
            raise ValidationError({'title': 'Author may have only one review for title'})
        serializer.save(author=author, title=title)

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        return title.reviews.all()


class CommentView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly | IsAdminOrIsModerator | IsAllowToView]

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()
