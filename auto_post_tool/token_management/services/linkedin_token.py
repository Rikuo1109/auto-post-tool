from datetime import datetime, timedelta
from token_management.models.token import LinkedInToken
from user_account.models.user import User
from utils.exceptions import NotFound, ValidationError
from utils.services.linkedin import LinkedInService

SUCCESS_CODE = 200


class LinkedInTokenService:
    """Get the value of access token from FE then turn it into a ThirdPartyToken Object in the DB
    Flow:
    1. get access from oath
    2. check access: expire
    4. deactivate
    5. reauthenticate"""

    @staticmethod
    def call_access_token_from_oauth(user: User, oath_code: str):
        """EXPECTED: oath_code returned from FE"""
        LinkedInTokenService.deactivate(user=user)
        response = LinkedInService.request_access_oath(oath_code=oath_code)
        if response.status_code == SUCCESS_CODE:
            response_data = response.json()
            LinkedInToken.create_token(
                user=user,
                exp=int(response_data.get("expires_in")),
                access_token=response_data.get("access_token"),
            )
        else:
            raise ValidationError(message_code="INVALID_OAUTH_TOKEN")

    @staticmethod
    def get_access_token(user: User):
        try:
            linkedin_token = LinkedInToken.objects.get(user=user, active=True)
        except LinkedInToken.DoesNotExist as exc:
            raise NotFound(message_code="TWITTER_NOT_CONNECTED") from exc
        return linkedin_token.access_token

    @staticmethod
    def create_token(user: User, access_token: str, exp: int):
        """function to create a facebook token"""
        linkedin_token = LinkedInToken(user=user, access_token=access_token)
        linkedin_token.expire_at = datetime.now() + timedelta(seconds=exp)
        linkedin_token.save()

    @staticmethod
    def deactivate(user: User):
        LinkedInToken.objects.filter(user=user, active=True).update(active=False)

    @staticmethod
    def check_exist_linkedin_token(user: User):
        return LinkedInToken.objects.filter(user=user, active=True).exists()

    @staticmethod
    def check_valid_linkedin_token(user: User, token: LinkedInToken):
        if token.expire_at >= datetime.now() or not token.active:
            LinkedInTokenService.deactivate(user=user)
            return False
        return True
