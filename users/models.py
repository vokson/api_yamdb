from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.role = MyUser.ADMIN
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLES = [
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user'),
    ]

    username = models.CharField(
        unique=True,
        max_length=150,
        verbose_name='Username',
        help_text='Input username',
        blank=False
    )

    email = models.EmailField(
        verbose_name='E-mail',
        help_text='Input e-mail',
        max_length=255,
        unique=True,
    )

    role = models.CharField(
        max_length=30,
        choices=ROLES,
        default=USER,
    )

    confirmation_code = models.CharField(
        max_length=128,
        verbose_name='Confirmation Code',
        help_text='Input confirmation code',
    )

    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='First Name',
        help_text='Input first name'
    )

    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Last Name',
        help_text='Input last name'
    )

    bio = models.TextField(
        blank=True,
        verbose_name='Description',
        help_text='Add description'
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['email']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
