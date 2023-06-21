from datetime import timedelta
from django.db import models
from django.conf import settings
from user_account.models.user import User
from utils.enums.post import PostManagementPlatFormEnum


class LoginToken(models.Model):
    """Model for JWT token"""

    token = models.TextField(editable=False, unique=True, primary_key=True)
    active = models.BooleanField(editable=True, default=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    deactivated_at = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)


class ResetToken(models.Model):
    """Model representing token given when issuing reset"""

    token = models.TextField(editable=False, max_length=64, primary_key=True)
    user_uid = models.ForeignKey(to=User, related_name="user", on_delete=models.CASCADE)
    active = models.BooleanField(editable=True, default=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    expire_at = models.DateTimeField(auto_now_add=False, auto_now=False)

    def save(self, *args, **kwargs):
        self.expire_at = self.created_at + timedelta(minutes=settings.RESET_PASSWORD_TOKEN_LIFETIME)
        super().save(*args, **kwargs)


class ThirdPartyToken(models.Model):
    """Model representing a token to save it in the database"""

    token = models.TextField(editable=False, unique=True, primary_key=True)
    platform = models.CharField(max_length=16, choices=PostManagementPlatFormEnum.choices)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    expire_time = models.DateTimeField(auto_now_add=False, auto_now=False)


# Create your models here.
