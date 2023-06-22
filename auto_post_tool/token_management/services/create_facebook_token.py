from datetime import timedelta

from django.conf import settings

import requests
from passlib.hash import pbkdf2_sha256
from token_management.models.token import FacebookToken
from utils.exceptions import ValidationError
from user_account.models.user import User

FACEBOOK_ACCESS_TOKEN_URL = "https://graph.facebook.com/oauth/access_token"


class FacebookTokenService:
    """Get the value of access token from FE then turn it into a ThirdPartyToken Object in the DB"""

    @staticmethod
    def create_token(exp: int, user: User, token: str):
        """function to create a facebook token"""
        encrypted_token = pbkdf2_sha256.hash(token)
        facebook_token = FacebookToken.objects.create(user=user, long_live_token=encrypted_token)
        facebook_token.expire_at = facebook_token.created_at + timedelta(seconds=exp)
        facebook_token.save()

    @staticmethod
    def get_long_lived_access_token(user_id, short_lived_access_token):
        """Generate long-live access token from short-live"""
        try:
            response = requests.post(
                FACEBOOK_ACCESS_TOKEN_URL,
                params={
                    "grant_type": "fb_exchange_token",
                    "client_id": settings.FACEBOOK_API_APP_ID,
                    "client_secret": settings.FACEBOOK_API_APP_SECRET,
                    "fb_exchange_token": short_lived_access_token,
                },
                headers={"Authorization": f"Bearer {short_lived_access_token}"},
                timeout=settings.REQUEST_TIMEOUT,
            )
        except TimeoutError as exc:
            raise TimeoutError("Request timed out") from exc

        if response.status_code == 200:
            FacebookTokenService.create_token(
                response.json().get("expires in"), user_id, response.json().get("access_token")
            )
        else:
            raise ValidationError(message_code="INVALID_FACEBOOK_TOKEN")