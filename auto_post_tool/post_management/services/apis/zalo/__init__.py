"""
Reference: https://developers.zalo.me/docs/api/official-account-api/gui-tin-va-thong-bao-qua-oa/v3/tin-truyen-thong/
"""
from django.conf import settings

import requests
from utils.exceptions import ValidationError


class ZaloOAService:
    def __init__(self, access_token, user_id):
        self.access_token = access_token
        self.user_id = user_id
        self.path = settings.ZALO_API_HOST

    def publish_feed(self, message: dict):
        """
        Zalo OA account senf promotion message to personal user
        """
        response = requests.post(
            self.path,
            headers={"access_token": self.access_token, "Content-Type": "application/json"},
            data={
                "type": "normal",
                "title": "Thời đại mới",
                "author": "Thời đại mới",
                # "cover": {"cover_type": "photo", "photo_url": "url", "status": "show"},
                "description": "This is news",
                "body": [{"type": "text", "content": "This is news"}, {"type": "text", "content": "This is news"}],
                "status": "show",
                "comment": "show",
            },
            timeout=settings.REQUEST_TIMEOUT,
        )
        if response.status_code == 200:
            return response
        else:
            raise ValidationError(message_code="CONTACT_ADMIN_FOR_SUPPORT")
