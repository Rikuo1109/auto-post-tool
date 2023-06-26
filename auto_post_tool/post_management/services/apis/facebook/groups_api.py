from enum import unique

from django.conf import settings
from django.db.models import TextChoices

import requests
from utils.exceptions import ValidationError


@unique
class PostTypeEnum(TextChoices):
    MARKDOWN = "MARKDOWN", "markdown"
    PLAINTEXT = "PLAINTEXT", "plaintext"


class GroupsApiFacebookService:
    def __init__(self, access_token, group_id):
        self.access_token = access_token
        self.group_id = group_id
        self.path = settings.FACEBOOK_API_HOST

    def get_users(self):
        response = requests.get(
            "/".join([self.path, self.group_id]),
            headers={"Authorization": f"Bearer {self.access_token}"},
            timeout=settings.REQUEST_TIMEOUT,
        )
        if response.status_code == 200:
            return response

    def publish_feed(self, message, formatting=PostTypeEnum.MARKDOWN):
        """
        Facebook does not support scheduled_publish_time
        """
        response = requests.post(
            "/".join([self.path, self.group_id, "feed"]),
            params={"access_token": self.access_token, "message": message, "formatting": formatting},
            timeout=settings.REQUEST_TIMEOUT,
        )
        if response.status_code == 200:
            return response
        else:
            raise ValidationError(message_code="CONTACT_ADMIN_FOR_SUPPORT")
