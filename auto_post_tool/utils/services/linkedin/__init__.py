from django.conf import settings

import requests


class LinkedInService(object):
    @staticmethod
    def get_response(data: str):
        return requests.request(
            "POST",
            settings.LINKEDIN_ACCESS_TOKEN_URL,
            headers={"Content-Type": settings.API_REQUEST_CONTENT_TYPE},
            data=data,
        )

    @staticmethod
    def request_access_oath(cls, oath_code: str):
        return LinkedInService.get_response(
            data={
                "code": oath_code,
                "grant_type": "authorization_code",
                "redirect_uri": settings.CALL_BACK_URL,
                "client_id": settings.LINKEDIN_CLIENT_ID,
                "client_secret": settings.LINKEDIN_CLIENT_SECRET,
            }
        )
