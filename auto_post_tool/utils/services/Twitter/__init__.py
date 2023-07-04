from django.conf import settings

import requests
from utils.encoding import EncodingService


class TwitterService(object):
    def __init__(self):
        self.client_id = settings.TWITTER_CLIENT_ID
        self.client_secret = settings.TWITTER_CLIENT_SECRET
        self.request_content_type = settings.API_REQUEST_CONTENT_TYPE

    def get_response(self, data={}):
        return requests.request(
            "POST",
            settings.TWITTER_ACCESS_TOKEN_URL,
            headers={
                "Content-Type": self.request_content_type,
                "Authorization": f"Basic {EncodingService.create_base64_auth_code(client_id=self.client_id, client_secret=self.client_secret)}",
            },
            data=data,
        )

    def request_access_oath(self, oath_code: str, code_verifier: str):
        return self.get_response(
            data={
                "code": oath_code,
                "grant_type": "authorization_code",
                "redirect_uri": settings.CALL_BACK_URL,
                "code_verifier": code_verifier,
            }
        )

    def request_access_fefresh(self, refresh_token: str):
        return self.get_response(data={"grant_type": "refresh_token", "refresh_token": refresh_token})
