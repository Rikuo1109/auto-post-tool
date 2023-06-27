from uuid import uuid4

from django.db import models


class ImagePost(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    source = models.ImageField()
    date_updated = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def filter_by_uids(uids: list):
        return ImagePost.objects.filter(uid__in=uids)
