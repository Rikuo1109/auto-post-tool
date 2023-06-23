import random
import string
from datetime import datetime

from django.conf import settings

from token_management.models.token import ResetToken
from user_account.models import User
from utils.exceptions.exceptions import ValidationError, NotFound


class CreateResetTokenService:
    """Get the value of Reset token then turn it into a ResetToken Object in the DB"""

    @staticmethod
    def generator_token():
        return "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(int(settings.RESET_TOKEN_LENGTH))
        )

    @staticmethod
    def create_reset_token(user: User):
        """Generate token for reseting password"""
        random_token = CreateResetTokenService.generator_token()

        while ResetToken.objects.filter(token=random_token).exists():
            random_token = CreateResetTokenService.generator_token()

        reset_token = ResetToken(token=random_token, user=user)
        reset_token.save()
        return random_token

    @staticmethod
    def deactivate(token: ResetToken):
        if not token.active:
            raise ValidationError("This token has already been deactivate")
        token.active = False
        token.save()

    @staticmethod
    def check_expired(token: ResetToken):
        return token.expire_at > datetime.now()
