from django.db import transaction

from token_management.models.token import Token


class RemoveTokenService:
    """Implement removing token given that it expired"""

    def __init__(self, uid):
        self.uid = uid

    @transaction.atomic
    def __call__(self):
        token = Token.objects.get(uid=self.uid)
        token.delete()
