import requests
from django.conf import settings


class ZaloService(object):
    def __init__(self, app_id: str, app_secret: str, request_content_type: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.request_content_type = request_content_type

    def generate_access_oath_data(self, oath_code: str):
        return f"app_id={self.app_id}&grant_type=authorization_code&code={oath_code}"

    def generate_access_fefresh_data(self, refresh_token: str):
        return f"app_id={self.app_id}&grant_type=refresh_token&code={refresh_token}"

    def get_request(self, request_name: str, code: str):
        """
        Args:
            request_name (str): 'authorization_code' OR 'refresh_token'
            code (str): oath_code or refresh_token

        Returns:
            Response: get access token response
        """
        return requests.request(
            "POST",
            settings.ZALO_ACCESS_TOKEN_URL,
            headers={
                "secret_key": settings.ZALO_API_SECRET_KEY,
                "Content-Type": settings.ZALO_API_REQUEST_CONTENT_TYPE,
            },
            data=self.generate_access_fefresh_data(refresh_token=code)
            if request_name == "refresh_token"
            else self.generate_access_oath_data(oath_code=code),
        )
