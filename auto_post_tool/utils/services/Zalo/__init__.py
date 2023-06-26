import requests
from django.conf import settings


class ZaloService(object):
    def __init__(self):
        self.app_id = settings.ZALO_API_APP_ID
        self.app_secret = settings.ZALO_API_APP_SECRET
        self.request_content_type = settings.ZALO_API_REQUEST_CONTENT_TYPE

    def get_response(self, data: str):
        return requests.request(
            "POST",
            settings.ZALO_ACCESS_TOKEN_URL,
            headers={
                "secret_key": settings.ZALO_API_APP_SECRET,
                "Content-Type": settings.ZALO_API_REQUEST_CONTENT_TYPE,
            },
            data=data,
        )

    def request_access_oath(self, oath_code: str):
        return self.get_response(data=f"app_id={self.app_id}&grant_type=authorization_code&code={oath_code}")

    def request_access_fefresh(self, refresh_token: str):
        return self.get_response(data=f"app_id={self.app_id}&grant_type=refresh_token&code={refresh_token}")
