from datetime import timedelta

from django.conf import settings
from django.db import models

from user_account.models.user import User


class LoginToken(models.Model):
    """Model for JWT token"""

    token = models.TextField(editable=False, unique=True, primary_key=True)
    active = models.BooleanField(editable=True, default=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    deactivated_at = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)


class ResetToken(models.Model):
    """Model representing token given when issuing reset"""

    token = models.TextField(editable=False, max_length=64, primary_key=True)
    user = models.ForeignKey(
        to=User,
        related_name="user_fk_user_account",
        on_delete=models.CASCADE,
        db_constraint=False,
        db_column="user_uid",
    )
    active = models.BooleanField(editable=True, default=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    expire_at = models.DateTimeField(auto_now_add=False, auto_now=False)

    def save(self, *args, **kwargs):
        self.expire_at = self.created_at + timedelta(minutes=settings.RESET_PASSWORD_TOKEN_LIFETIME)
        super().save(*args, **kwargs)


class FacebookToken(models.Model):
    """Model representing a token to save it in the database
    after long-live-token expire, request new shirt-live to get new long-live
    """

    long_live_token = models.TextField(editable=False, unique=True, primary_key=True)
    user_uid = models.ForeignKey(to=User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    expire_at = models.DateTimeField()


class ZaloToken(models.Model):
    """Model representing a zalo token
    First get new access & token
    When access expired, use refresh to create new access, active = False
    When access expire again, get new access & refresh"""

    access_token = models.TextField(editable=False, unique=True, primary_key=True)
    refresh_token = models.TextField(editable=False, unique=False)
    user_uid = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    expire_at = models.DateTimeField()
