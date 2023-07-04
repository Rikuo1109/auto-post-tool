from django.conf import settings
from token_management.models.token import User
from token_management.services.linkedin_token import LinkedInTokenService
import requests


class LinkedInService(object):
    @staticmethod
    def return_response(url: str, header: str, data={}, method="POST"):
        return requests.request(method=method, url=url, headers=header, data=data)

    @staticmethod
    def request_access_oath(oath_code: str):
        return LinkedInService.return_response(
            method="POST",
            url=settings.LINKEDIN_ACCESS_TOKEN_URL,
            headers={"Content-Type": settings.API_REQUEST_CONTENT_TYPE},
            data={
                "code": oath_code,
                "grant_type": "authorization_code",
                "redirect_uri": settings.CALL_BACK_URL,
                "client_id": settings.LINKEDIN_CLIENT_ID,
                "client_secret": settings.LINKEDIN_CLIENT_SECRET,
            },
        )

    @staticmethod
    def get_user_info(user: User):
        return LinkedInService.return_response(
            method="GET",
            url=settings.LINKEDIN_SELF_PROFILE_URL,
            header={"Authorization": f"Bearer {LinkedInTokenService.get_access_token(user=user)}"},
        )
