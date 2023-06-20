from django.db import transaction

from token_management.models.token import ThirdPartyToken


class Create3rdTokenService:
    """Get the value of access token from FE then turn it into a ThirdPartyToken Object in the DB"""

    def __init__(self, value, platform, created_at, expire_at):
        self.value = value
        self.platform = platform
        self.created_at = created_at
        self.expire_at = expire_at

    @transaction.atomic
    def __call__(self):
        token = ThirdPartyToken.objects.create(
            value=self.value, platform=self.platform, created_at=self.created_at, expire_at=self.expire_at
        )
        token.save()
