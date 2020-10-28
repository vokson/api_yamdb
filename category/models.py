from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Categories(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['slug']

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['slug']

    def __str__(self):
        return self.name


class Titles(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, related_name='title')
    genre = models.ManyToManyField(Genres)
    name = models.CharField(max_length=50)
    year = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=50)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.name
