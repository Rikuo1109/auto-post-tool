from typing import List
from uuid import uuid4

from django.db import models

from utils.exceptions import NotFound


class ImagePost(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    source = models.ImageField()
    date_updated = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_by_uid(uid: str):
        try:
            return ImagePost.objects.get(uid=uid)
        except ImagePost.DoesNotExist as e:
            raise NotFound(message_code="IMAGE_NOT_FOUND") from e

    @staticmethod
    def filter_by_uids(uids: List[str]):
        try:
            return ImagePost.objects.filter(uid__in=uids)
        except ImagePost.DoesNotExist as e:
            raise NotFound(message_code="IMAGE_NOT_FOUND") from e
