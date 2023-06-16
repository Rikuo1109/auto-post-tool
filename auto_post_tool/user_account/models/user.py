from __future__ import annotations

import logging
from typing import Any, Optional

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


LOGGER = logging.getLogger("API")


class UserManager(BaseUserManager):  # type: ignore
    def create_user(self, email: str, password: Optional[str]) -> Any:
        if not email:
            raise ValueError("Users must have an email address")

        user: Any = User(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: Optional[str]) -> Any:
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        print("Superuser created successfully.")
        return user


class User(AbstractUser):
    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS: list[str] = []

    username = None

    email = models.EmailField(unique=True, verbose_name="email-address", max_length=255)

    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)

    # Other information
    country = models.CharField(max_length=255, blank=True, null=True)

    # Required by django admin
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)

    last_login = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now=False, auto_now_add=True)