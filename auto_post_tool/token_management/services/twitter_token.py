from datetime import datetime, timedelta

from token_management.models.token import TwitterToken
from user_account.models.user import User
from utils.exceptions import NotFound, ValidationError
from utils.services.twitter import TwitterService


class TwitterTokenService:
    """Get the value of access token from FE then turn it into a ThirdPartyToken Object in the DB
    Flow:
    1. get access from oath
    2. check access: expire
    3. get refresh
    4. deactivate
    5. get access from refresh"""

    @staticmethod
    def call_access_token_from_oauth(user: User, oath_code: str, code_verifier: str):
        """EXPECTED: oath_code returned from FE"""
        TwitterTokenService.deactivate(user=user)
        response = TwitterService().request_access_oath(oath_code=oath_code, code_verifier=code_verifier)
        if response.status_code == 200:
            response_data = response.json()
            TwitterTokenService.create_token(
                user=user,
                exp=int(response_data.get("expires_in")),
                access_token=response_data.get("access_token"),
                refresh_token=response_data.get("refresh_token"),
            )
        else:
            raise ValidationError(message_code="INVALID_OAUTH_TOKEN")

    @staticmethod
    def get_access_token(user: User):
        try:
            twitter_token = TwitterToken.objects.get(user=user, active=True)
        except TwitterToken.DoesNotExist as exc:
            raise NotFound(message_code="TWITTER_NOT_CONNECTED") from exc
        return twitter_token.access_token

    @staticmethod
    def get_refresh_token(user: User):
        try:
            twitter_token = TwitterToken.objects.get(user=user, active=True)
        except TwitterToken.DoesNotExist as exc:
            raise NotFound(message_code="TWITTER_NOT_CONNECTED") from exc
        return twitter_token.refresh_token

    @staticmethod
    def call_access_token_from_refresh(user: User, refresh_token: str):
        TwitterTokenService.deactivate(user=user)
        response = TwitterService().request_access_fefresh(refresh_token=refresh_token)
        if response.status_code == 200:
            response_data = response.json()
            TwitterTokenService.create_token(
                user=user,
                exp=int(response_data.get("expires_in")),
                access_token=response_data.get("access_token"),
                refresh_token=response_data.get("refresh_token"),
            )
        else:
            raise ValidationError(message_code="INVALID_TWITTER_REFRESH_TOKEN")

    @staticmethod
    def create_token(user: User, access_token: str, refresh_token: str, exp: int):
        """function to create a facebook token"""
        twitter_token = TwitterToken(user=user, access_token=access_token, refresh_token=refresh_token)
        twitter_token.expire_at = datetime.now() + timedelta(seconds=exp)
        twitter_token.save()

    @staticmethod
    def deactivate(user: User):
        TwitterToken.objects.filter(user=user, active=True).update(active=False)

    @staticmethod
    def check_exist_zalo_token(user: User):
        return TwitterToken.objects.filter(user=user, active=True).exists()

    @staticmethod
    def check_valid_zalo_token(user: User, token: TwitterToken):
        if token.expire_at >= datetime.now() or not token.active:
            TwitterTokenService.deactivate(user=user)
            return False
        return True
