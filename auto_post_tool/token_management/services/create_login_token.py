import jwt

from datetime import datetime, timedelta
from django.conf import settings
from token_management.models.token import LoginToken
from user_account.models.user import User
from utils.exceptions.exceptions import ValidationError

class CreateLoginTokenService:
    """Get the value of JWT token then turn it into a LoginToken Object in the DB"""

    @staticmethod
    def generator_token(uid: str):
        return jwt.encode(
            {"user_uid": uid, "exp": datetime.now() + timedelta(minutes=int(settings.JWT_EXPIRED_TIME))},
            settings.SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    @staticmethod
    def create_token(user: User):
        """function to create a jwt token for logging in"""
        access_token = CreateLoginTokenService.generator_token(uid=str(user.uid))
        jwt_token = LoginToken(user=user, token=access_token)
        jwt_token.save()
        return access_token
    
    @staticmethod
    def deactivate(token: str):
        try:
            login_token = LoginToken.objects.get(token=token)
        except LoginToken.MultipleObjectsReturned:
            raise ValidationError(message_code="CONTACT_ADMIN_FOR_SUPPORT")

        login_token.active = False
        login_token.deactivate_at = datetime.now()
        login_token.save()
