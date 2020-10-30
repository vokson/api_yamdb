from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from category.models import Titles

User = get_user_model()


class Review(models.Model):
    text = models.TextField(max_length=500)
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews'
    )


class Comment(models.Model):
    text = models.TextField(max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
