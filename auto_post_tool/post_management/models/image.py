from uuid import uuid4

from django.conf import settings
from django.db import models


class Image:
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    name = models.CharField(max_length=150)
    source = models.ImageField(upload_to=settings.MEDIA_URL)
    date_updated = models.DateTimeField(auto_now_add=True)
