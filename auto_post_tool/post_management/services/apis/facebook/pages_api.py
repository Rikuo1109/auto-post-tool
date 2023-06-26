from django.conf import settings

import requests
from utils.exceptions import ValidationError


class PagesApiFacebookService:
    def __init__(self, access_token, page_id):
        self.access_token = access_token
        self.page_id = page_id
        self.path = settings.FACEBOOK_API_HOST

    def get_feed_in_page(self):
        response = requests.get(
            "/".join([self.path, self.page_id]),
            headers={"Authorization": f"Bearer {self.access_token}"},
            timeout=settings.REQUEST_TIMEOUT,
        )
        if response.status_code == 200:
            return response

    def publish_feed(self, message, published=True, scheduled_publish_time_unix_timestamp: float = None):
        """Permission
        * pages_manage_posts
        * pages_read_engagement
        * Page access token
        """
        params = {"access_token": self.access_token, "message": message, "published": published}
        if scheduled_publish_time_unix_timestamp is not None:
            params["published"] = False
            params["scheduled_publish_time"] = scheduled_publish_time_unix_timestamp

        response = requests.post(
            "/".join([self.path, self.page_id, "feed"]), params=params, timeout=settings.REQUEST_TIMEOUT
        )

        if response.status_code == 200:
            return response
        elif response.status_code == 400:
            response_code = response.json().get("code")
            if response_code == 100:
                raise ValidationError(message_code="INVALID_SCHEDULED_PUBLISH_TIME")
            elif response_code == 190:
                raise ValidationError(message_code="INVALID_FACEBOOK_TOKEN")
        else:
            raise ValidationError(message_code="CONTACT_ADMIN_FOR_SUPPORT")
