from django.db import transaction

from token_management.models.token import Token


class RemoveTokenService:
    """Implement removing token given that it expired"""

    def __init__(self, value):
        self.value = value

    @transaction.atomic
    def __call__(self):
        token = Token.objects.get(value=self.value)
        token.delete()
