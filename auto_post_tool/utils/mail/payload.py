from datetime import datetime

from django.conf import settings
from django.template.loader import render_to_string

from token_management.services.create_reset_token import ResetTokenService
from user_account.models import User


BASE_MEDIA_HOST = settings.BASE_MEDIA_HOST
BASE_UI_URL = settings.BASE_UI_URL


class EmailPayload:
    @staticmethod
    def reset_password(user: User):
        """
        Activate user email payload.
        """
        email = user.email
        subject = "Đặt lại mật khẩu"

        reset_token = ResetTokenService().create_reset_token(user=user)

        context = {
            "last_name": user.last_name,
            "first_name": user.first_name,
            "time": datetime.now,
            "reset_link": f"{settings.BASE_UI_URL}/reset-password/{reset_token}",
            "base_ui_url": BASE_UI_URL,
            "username": user.username,
        }

        body = render_to_string("forgot_password_email.html", context)

        return subject, body, email
