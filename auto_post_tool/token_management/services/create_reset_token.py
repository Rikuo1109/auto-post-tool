from django.db import transaction

from token_management.models.token import ResetToken


class CreateResetTokenService:
    """Get the value of Reset token then turn it into a ResetToken Object in the DB"""

    def __init__(self, token, active, created_at, expire_at):
        self.token = token
        self.active = active
        self.created_at = created_at
        self.expire_at = expire_at

    @transaction.atomic
    def __call__(self):
        token = ResetToken.objects.create(
            token=self.token, active=self.active, created_at=self.created_at, expire_at=self.expire_at
        )
        token.save()
