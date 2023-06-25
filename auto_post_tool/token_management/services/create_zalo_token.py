import requests
from datetime import timedelta, datetime
from django.conf import settings
from passlib.hash import pbkdf2_sha256
from token_management.models.token import ZaloToken
from user_account.models.user import User
from utils.exceptions import ValidationError, NotFound
from utils.services.Zalo import ZaloService

ZALO_ACCESS_TOKEN_URL = "https://oauth.zaloapp.com/v4/oa/access_token"


class ZaloTokenService:
    """Get the value of access token from FE then turn it into a ThirdPartyToken Object in the DB"""

    @staticmethod
    def call_access_token_from_oauth(user: User, oath_code: str):
        """EXPECTED: oath_code returned from FE"""
        if ZaloToken.objects.filter(user=user, active=True).exists():
            ZaloTokenService.deactivate(user=user)
        response = requests.request(
            "POST",
            ZALO_ACCESS_TOKEN_URL,
            headers={
                "secret_key": settings.ZALO_API_APP_SECRET,
                "Content-Type": settings.ZALO_API_APP_REQUEST_CONTENT_TYPE,
            },
            data=ZaloService.generate_access_oath_link(oath_code=oath_code),
        )
        if response.status_code == 200:
            response_data = response.json()
            ZaloTokenService.create_token(
                exp=response_data.get("expires_in"),
                user=user,
                access_token=response_data.get("access_token"),
                refresh_token=response_data.get("refresh_token"),
            )
        else:
            raise ValidationError(message_code="INVALID_OAUTH_TOKEN")

    @staticmethod
    def get_refresh_token(user: User):
        try:
            zalo_token = ZaloToken.objects.get(user=user, active=True)
        except ZaloToken.DoesNotExist as exc:
            raise NotFound(message_code="ZALO_TOKEN_NOT_CONNECTED")
        return zalo_token.refresh_token

    @staticmethod
    def call_access_token_from_refresh(user: User):
        if ZaloToken.objects.filter(user=user, active=True).exists():
            ZaloTokenService.deactivate(user=user)
        response = requests.request(
            "POST",
            ZALO_ACCESS_TOKEN_URL,
            headers={
                "secret_key": settings.ZALO_API_APP_SECRET,
                "Content-Type": settings.ZALO_API_APP_REQUEST_CONTENT_TYPE,
            },
            data=ZaloService.generate_access_fefresh_link(refresh_token=ZaloTokenService.get_refresh_token(user=user)),
        )
        if response.status_code == 200:
            response_data = response.json()
            ZaloTokenService.create_token(
                exp=response_data.get("expires_in"),
                user=user,
                access_token=response_data.get("access_token"),
                refresh_token=response_data.get("refresh_token"),
            )
        else:
            raise ValidationError(message_code="INVALID_ZALO_REFRESH_TOKEN")

    @staticmethod
    def create_token(exp: str, user: User, access_token: str, refresh_token: str):
        """function to create a facebook token"""
        encrypted_access_token = pbkdf2_sha256.hash(access_token)
        encrypted_refresh_token = pbkdf2_sha256.hash(refresh_token)
        zalo_token = ZaloToken(user=user, access_token=encrypted_access_token, refresh_token=encrypted_refresh_token)
        zalo_token.expire_at = datetime.now() + timedelta(seconds=exp)
        zalo_token.save()

    @staticmethod
    def deactivate(user: User):
        ZaloToken.objects.filter(user=user, active=True).update(active=False)

    @staticmethod
    def check_exist_zalo_token(user: User):
        return ZaloToken.objects.filter(user=user, active=True).exists()

    @staticmethod
    def check_valid_zalo_token(token: ZaloToken):
        return token.expire_at < datetime.now() and token.active
