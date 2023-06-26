from django.conf import settings

import requests
from utils.exceptions import ValidationError
from ..helper_functions import *


class PagesFacebookApiService:
    def __init__(self, post_management):
        self.post_management = post_management
        user = post_management.post.user
        self.page_id = get_page_id_facebook(user=user)
        self.access_token = get_page_access_token_facebook(user=user)
        self.path = settings.FACEBOOK_API_HOST

    def get_feed_in_page(self):
        response = requests.get(
            "/".join([self.path, self.page_id]),
            headers={"Authorization": f"Bearer {self.access_token}"},
            timeout=settings.REQUEST_TIMEOUT,
        )
        if response.status_code == 200:
            return response

    def prepair_params(self):
        message = self.post_management.post.content
        published = self.post_management.auto_publish
        if self.post_management.time_posting is None:
            raise ValidationError(message_code="INVALID_SCHEDULED_PUBLISH_TIME")
        scheduled_publish_time_unix_timestamp = self.post_management.time_posting.timestamp()

        params = {"access_token": self.access_token, "message": message, "published": published}

        if scheduled_publish_time_unix_timestamp is not None:
            params["published"] = False
            params["scheduled_publish_time"] = scheduled_publish_time_unix_timestamp

        return params

    def publish_feed(self):
        """Permission
        * pages_manage_posts
        * pages_read_engagement
        * Page access token
        """
        params = self.prepair_params()

        response = requests.post(
            "/".join([self.path, self.page_id, "feed"]), params=params, timeout=settings.REQUEST_TIMEOUT
        )

        return self.handle_response(response)

    def handle_response(self, response):
        if response.status_code == 200:
            return response
        elif response.status_code == 400:
            response_code = response.json().get("code")
            if response_code == 100:
                raise ValidationError(message_code="INVALID_SCHEDULED_PUBLISH_TIME")
            elif response_code == 190:
                raise ValidationError(message_code="INVALID_FACEBOOK_TOKEN")
        raise ValidationError(message_code="CONTACT_ADMIN_FOR_SUPPORT")
