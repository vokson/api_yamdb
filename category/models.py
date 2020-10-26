from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Categories(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, related_name='title')
    genre = models.ManyToManyField(Genres)
    name = models.CharField(max_length=50)
    year = models.PositiveSmallIntegerField()
    # rating = models.IntegerField(default=None)
    description = models.CharField(max_length=50)
