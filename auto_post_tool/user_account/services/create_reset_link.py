from django.conf import settings
from token_management.models.token import ResetToken


class CreateResetLinkService:
    def create_reset_link(self,token):
        return f"{settings.FRONTEND_HOST_URL}/reset-password/{token}"
        
