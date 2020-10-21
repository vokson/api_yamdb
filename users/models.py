from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from loguru import logger
import random

random_string = str(random.randint(10000, 99999))

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        logger.debug(user)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(
        unique=True,
        max_length=150,
        verbose_name='Username',
        help_text='Input username',
        null=True,
    )

    email = models.EmailField(
        verbose_name='E-mail',
        help_text='Input e-mail',
        max_length=255,
        unique=True,
    )

    confirmation_code = models.CharField(
        max_length=128,
        blank=False,
        verbose_name='Confirmation Code',
        help_text='Input confirmation code',
        default=random_string
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

    description = models.TextField(
        blank=True,
        verbose_name='Description',
        help_text='Add description'
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
