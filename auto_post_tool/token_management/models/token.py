from uuid import uuid4

from django.db import models

from user_account.models.user import User
from utils.enums.post import PostManagementPlatFormEnum


class Token(models.Model):
    """Model representing a token to save it in the database"""

    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=16, choices=PostManagementPlatFormEnum.choices)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    expire_time = models.DateTimeField(auto_now_add=False, auto_now=False)


# Create your models here.
