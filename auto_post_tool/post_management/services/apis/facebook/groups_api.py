from enum import unique

from django.conf import settings
from django.db.models import TextChoices

import requests
from utils.exceptions import ValidationError


@unique
class PostTypeEnum(TextChoices):
    MARKDOWN = "MARKDOWN", "markdown"
    PLAINTEXT = "PLAINTEXT", "plaintext"


class GroupsFacebookApiService:
    def __init__(self, post_management):
        self.post_management = post_management
        user = post_management.post.user
        self.group_id = "1034782201238472"
        self.access_token = "<YOUR_ACCESS_TOKEN>"
        self.path = settings.FACEBOOK_API_HOST
        self.image_ids = list()

    def get_users(self):
        response = requests.get(
            "/".join([self.path, self.group_id]),
            headers={"Authorization": f"Bearer {self.access_token}"},
            timeout=settings.REQUEST_TIMEOUT,
        )
        if response.status_code == 200:
            return response

    def prepair_params_feed(self):
        return {
            "access_token": self.access_token,
            "message": self.post_management.post.content,
            "formatting": PostTypeEnum.MARKDOWN,
            "attached_media": [{"media_fbid": image_id} for image_id in self.image_ids],
        }

    def prepair_params_photos(self, url):
        return {"url": url, "published": False}

    def publish_image(self, source):
        params = self.prepair_params_photos(url=source)

        response = requests.post(
            "/".join([self.path, self.group_id, "photos"]), params=params, timeout=settings.REQUEST_TIMEOUT
        )

        return self.handle_response(response)

    def publish_feed(self):
        """
        Facebook does not support scheduled_publish_time
        """
        self.image_ids = []
        for image in self.post_management.post.images.all():
            self.image_ids.append(self.publish_image(source=image.source)["id"])
        params = self.prepair_params_feed(self.image_ids)
        response = requests.post(
            "/".join([self.path, self.group_id, "feed"]), params=params, timeout=settings.REQUEST_TIMEOUT
        )

        return self.handle_response(response)

    def handle_response(self, response):
        if response.status_code == 200:
            return response
        elif response.status_code == 400:
            response_code = response.json().get("error").get("code")
            if response_code == 190:
                raise ValidationError(message_code="INVALID_FACEBOOK_TOKEN")
            if response_code == 200:
                raise ValidationError(message_code="USER_DOES_NOT_HAVE_PERMISSIONS")
        raise ValidationError(message_code="CONTACT_ADMIN_FOR_SUPPORT")
