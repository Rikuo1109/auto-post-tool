from datetime import datetime, timedelta

from django.conf import settings

import requests
from token_management.models.token import FacebookToken, Group
from user_account.models.user import User
from utils.exceptions import NotAuthenticated, ValidationError, NotFound


class FacebookTokenService:
    """Get the value of access token from FE then turn it into a ThirdPartyToken Object in the DB"""

    @staticmethod
    def create_token(exp: int, user: User, token: str):
        """function to create a facebook token in the DB"""
        facebook_token = FacebookToken.objects.create(user=user, long_live_token=token)
        facebook_token.expire_at = datetime.now() + timedelta(seconds=exp)
        facebook_token.save()

    @staticmethod
    def get_long_lived_access_token(user: User, short_lived_access_token: str):
        """Generate long-live access token from short-live"""
        FacebookTokenService.deactivate(user=user)
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
                exp=int(response_data.get("expires_in")), user=user, token=response_data.get("access_token")
            )
        else:
            raise ValidationError(message_code="INVALID_FACEBOOK_TOKEN")

    @staticmethod
    def get_token_by_user(user: User):
        try:
            facebook_token = FacebookToken.objects.get(user=user, active=True)
        except FacebookToken.DoesNotExist as exc:
            raise NotAuthenticated(message_code="FACEBOOK_TOKEN_NOT_CONNECTED") from exc
        return facebook_token.long_live_token

    @staticmethod
    def deactivate(user: User):
        FacebookToken.objects.filter(user=user, active=True).update(active=False)

    @staticmethod
    def check_exist_facebook_token(user: User):
        return FacebookToken.objects.filter(user=user, active=True).exists()

    @staticmethod
    def check_valid_facebook_token(token: FacebookToken):
        return token.expire_at < datetime.now() and token.active
