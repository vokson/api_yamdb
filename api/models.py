from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Role(models.TextChoices):
    ADMIN = 'admin', 'admin'
    MODERATOR = 'moderator', 'moderator'
    USER = 'user', 'user'


class MyUser(AbstractUser):
    email = models.EmailField(
        verbose_name='E-mail',
        help_text='Input e-mail',
        unique=True,
    )

    role = models.CharField(
        verbose_name='Role',
        help_text='Choose role',
        max_length=30,
        choices=Role.choices,
        default=Role.USER
    )

    confirmation_code = models.CharField(
        max_length=128,
        verbose_name='Confirmation Code',
        help_text='Input confirmation code',
    )

    bio = models.TextField(
        blank=True,
        verbose_name='Description',
        help_text='Add description'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['email']

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.role == Role.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == Role.MODERATOR


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['slug']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['slug']

    def __str__(self):
        return self.name


class Title(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, related_name='title')
    genre = models.ManyToManyField(Genre)
    name = models.CharField(max_length=50)
    year = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=50)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.name


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
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        ordering = ['-pub_date']


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

    class Meta:
        ordering = ['-pub_date']
