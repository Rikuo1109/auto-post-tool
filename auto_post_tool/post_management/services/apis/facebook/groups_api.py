from enum import unique
from typing import List

from django.conf import settings
from django.db.models import TextChoices

import requests
from ..helper_functions import *
from utils.exceptions import ValidationError


@unique
class PostTypeEnum(TextChoices):
    MARKDOWN = "MARKDOWN", "markdown"
    PLAINTEXT = "PLAINTEXT", "plaintext"


class GroupsFacebookApiService:
    def __init__(self, post_management):
        self.post_management = post_management
        user = post_management.post.user
        self.group_id = get_group_id_facebook(user=user)
        self.access_token = get_user_access_token_facebook(user=user)
        self.path = settings.FACEBOOK_API_HOST

    def get_users(self):
        response = requests.get(
            "/".join([self.path, self.group_id]),
            headers={"Authorization": f"Bearer {self.access_token}"},
            timeout=settings.REQUEST_TIMEOUT,
        )
        if response.status_code == 200:
            return response

    def prepair_params_feed(self, image_ids: List = []):
        return {
            "access_token": self.access_token,
            "message": self.post_management.post.content,
            "formatting": PostTypeEnum.MARKDOWN,
            "attached_media": [{"media_fbid": image_id} for image_id in image_ids],
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
        image_ids = [self.publish_image(source=image.source)["id"] for image in self.post_management.post.images]
        params = self.prepair_params_feed(image_ids)

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
        raise ValidationError(message_code="CONTACT_ADMIN_FOR_SUPPORT")
