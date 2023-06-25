from datetime import timedelta, datetime

from django.conf import settings

import requests
from passlib.hash import pbkdf2_sha256
from token_management.models.token import FacebookToken
from utils.exceptions import ValidationError, PermissionDenied
from user_account.models.user import User


class FacebookTokenService:
    """Get the value of access token from FE then turn it into a ThirdPartyToken Object in the DB"""

    @staticmethod
    def create_token(exp: int, user: User, token: str):
        """function to create a facebook token in the DB"""
        encrypted_token = pbkdf2_sha256.hash(token)
        facebook_token = FacebookToken.objects.create(user=user, long_live_token=encrypted_token)
        facebook_token.expire_at = datetime.now() + timedelta(seconds=exp)
        facebook_token.save()

    @staticmethod
    def get_long_lived_access_token(user: User, short_lived_access_token: str):
        """Generate long-live access token from short-live
        Current logic: if token already exist, raise error
        Suggest new logic: if exist, deactivate then call new short-live -> new long-live"""
        if FacebookToken.objects.filter(user=user, active=True).exists():
            raise PermissionDenied(message_code="PERMISSION_DENIED")
        try:
            response = requests.post(
                settings.FACEBOOK_ACCESS_TOKEN_URL,
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
            response_data = response.json()
            FacebookTokenService.create_token(
                exp=response_data.get("expires_in"), user=user, token=response_data.get("access_token")
            )
        else:
            raise ValidationError(message_code="INVALID_FACEBOOK_TOKEN")

    @staticmethod
    def deactivate(user: User):
        FacebookToken.objects.filter(user=user, active=True).update(active=False)

    @staticmethod
    def check_exist_facebook_token(user: User):
        return FacebookToken.objects.filter(user=user, active=True).exists()

    @staticmethod
    def check_valid_facebook_token(token: FacebookToken):
        return token.expire_at < datetime.now() and token.active
