from datetime import timedelta, datetime
from uuid import uuid4
from django.conf import settings
from django.db import models

from user_account.models.user import User


class LoginToken(models.Model):
    """Model for JWT token"""

    uid = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(
        to=User, related_name="login_token_fk_user", on_delete=models.CASCADE, db_constraint=False, db_column="user_uid"
    )
    token = models.TextField(max_length=64, unique=True, null=False, blank=False)
    active = models.BooleanField(default=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, null=False, blank=False)
    deactivated_at = models.DateTimeField(null=True)


class ResetToken(models.Model):
    """Model representing token given when issuing reset"""

    uid = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(
        to=User, related_name="reset_token_fk_user", on_delete=models.CASCADE, db_constraint=False, db_column="user_uid"
    )
    token = models.TextField(max_length=64, null=False, blank=False)
    active = models.BooleanField(default=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    expire_at = models.DateTimeField(null=True, blank=False)

    def save(self, *args, **kwargs):
        self.expire_at = datetime.now() + timedelta(minutes=settings.RESET_PASSWORD_TOKEN_LIFETIME)
        super().save(*args, **kwargs)


class FacebookToken(models.Model):
    """Model representing a token to save it in the database
    after long-live-token expire, request new shirt-live to get new long-live
    """

    uid = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(
        to=User,
        related_name="facebook_token_fk_user",
        on_delete=models.CASCADE,
        db_constraint=False,
        db_column="user_uid",
    )
    long_live_token = models.TextField(unique=True, null=False, blank=False)
    active = models.BooleanField(default=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, null=False, blank=False)
    expire_at = models.DateTimeField(null=True, blank=False)


class ZaloToken(models.Model):
    """Model representing a zalo token
    First get new access & refresh token
    When access expired, use refresh to create new access & refresh, active = False
    """

    uid = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(
        to=User, related_name="zalo_token_fk_user", on_delete=models.CASCADE, db_constraint=False, db_column="user_uid"
    )
    access_token = models.TextField(unique=True, null=False, blank=False)
    refresh_token = models.TextField(unique=False, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    active = models.BooleanField(default=True, null=False, blank=False)
    expire_at = models.DateTimeField(null=True, blank=False)


class TwitterToken(models.Model):
    """Model representing a twitter token
    First get new access & refresh token
    When access expired, use refresh to create new access & refresh, active = False
    """

    uid = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(
        to=User,
        related_name="twitter_token_fk_user",
        on_delete=models.CASCADE,
        db_constraint=False,
        db_column="user_uid",
    )
    access_token = models.TextField(unique=True, null=False, blank=False)
    refresh_token = models.TextField(unique=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    active = models.BooleanField(default=True, null=False, blank=False)
    expire_at = models.DateTimeField(null=True, blank=False)
