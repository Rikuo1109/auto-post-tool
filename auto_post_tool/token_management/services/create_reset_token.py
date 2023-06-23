import random
import string

from django.conf import settings
from datetime import datetime
from token_management.models.token import ResetToken
from user_account.models import User
from utils.exceptions import ValidationError


class ResetTokenService:
    """Get the value of Reset token then turn it into a ResetToken Object in the DB"""

    @staticmethod
    def generator_token():
        return "".join(
            random.choice(string.ascii_letters + string.digits)
            for _ in range(int(settings.RESET_PASSWORD_TOKEN_LENGTH))
        )

    @staticmethod
    def create_reset_token(user: User):
        """Generate token for reseting password"""
        random_token = ResetTokenService.generator_token()

        while ResetToken.objects.filter(token=random_token).exists():
            random_token = ResetTokenService.generator_token()

        reset_token = ResetToken(token=random_token, user=user)
        reset_token.save()
        return random_token

    @staticmethod
    def deactivate(token: ResetToken):
        if not ResetTokenService.check_valid(token=token):
            raise ValidationError("VALIDATION_ERROR")
        token.active = False
        token.save()

    @staticmethod
    def check_valid(token: ResetToken):
        return token.expire_at > datetime.now() and token.active

