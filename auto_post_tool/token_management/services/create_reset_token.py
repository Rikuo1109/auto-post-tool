import random
import string
from django.conf import settings

from token_management.models.token import ResetToken


class CreateResetTokenService:
    """Get the value of Reset token then turn it into a ResetToken Object in the DB"""

    def create_reset_token(self, uid):
        random_token = "".join(
            random.choice(string.ascii_letters + string.digits)
            for i in range(int(settings.RESET_PASSWORD_TOKEN_LENGTH))
        )
        reset_token = ResetToken(token=random_token, user_uid=uid)
        reset_token.save()
        return random_token
