from django.db import transaction

from token_management.models.token import Token


class CreateTokenService:
    """Get the value of token from FE then turn it into a Token Object in the DB"""

    def __init__(self, value, browser, user, platform, created_at, expire_at):
        self.value = value
        self.browser = browser
        self.user = user
        self.platform = platform
        self.created_at = created_at
        self.expire_at = expire_at

    @transaction.atomic
    def __call__(self):
        token = Token.objects.create(
            value=self.value,
            browser=self.browser,
            user=self.user,
            platform=self.platform,
            created_at=self.created_at,
            expire_at=self.expire_at,
        )
        token.save()
