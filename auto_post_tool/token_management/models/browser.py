from uuid import uuid4
from django.db import models

from user_account.models.user import User


class Browser(models.Model):
    """Each user can use many browsers to access"""

    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    deviceName = models.CharField(max_length=64)
