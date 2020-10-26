from django.shortcuts import get_object_or_404

from rest_framework import viewsets

from socials.models import Review
from socials.permissions import IsAuthorOrReadOnly
from socials.serializers import ReviewSerializer, CommentSerializer


# TODO:
#  1. change response to NO paginated data
#  2. change permission from IsAuthorOrReadOnly to IsAuthorOrReadOnly and IsModerator and IsAdmin

class ReviewView(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()
