import random
import string
from datetime import datetime

from django.conf import settings
from datetime import datetime
from token_management.models.token import RegisterToken
from user_account.models import User
from utils.exceptions import ValidationError, NotFound


class RegisterTokenService:
    """Get the value of Register token then turn it into a RegisterToken Object in the DB"""

    @staticmethod
    def generator_token():
        return "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(settings.REGISTER_TOKEN_LENGTH)
        )

    @staticmethod
    def create_register_token(user: User):
        """Generate token for reseting password"""
        random_token = RegisterTokenService.generator_token()

        while RegisterToken.objects.filter(token=random_token).exists():
            random_token = RegisterTokenService.generator_token()

        register_token = RegisterToken(token=random_token, user=user)
        register_token.save()
        return random_token

    @staticmethod
    def deactivate(token: RegisterToken):
        if not RegisterTokenService.check_valid(token=token):
            raise ValidationError("VALIDATION_ERROR")
        token.active = False
        token.save()

    @staticmethod
    def check_valid(token: RegisterToken):
        if not token.expire_at:
            return False
        return token.expire_at > datetime.now() and token.active

    @staticmethod
    def get_token_by_user(user: User):
        try:
            register_token = RegisterToken.objects.get(user=user, active=True)
        except RegisterToken.DoesNotExist as exc:
            raise NotFound(message_code="USER_NOT_FOUND") from exc
        return register_token
