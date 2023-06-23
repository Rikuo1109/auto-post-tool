from uuid import uuid4

from django.db import models
from post_management.models.post import Post


class ImagePost(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    source = models.ImageField()
    date_updated = models.DateTimeField(auto_now_add=True)
