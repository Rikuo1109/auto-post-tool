# payload.py
from datetime import datetime

from django.conf import settings
from django.template.loader import render_to_string

from token_management.services.create_reset_token import CreateResetTokenService
from user_account.models import User
from user_account.services.create_reset_link import CreateResetLinkService


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

        reset_token = CreateResetTokenService().create_reset_token(user)
        reset_link = CreateResetLinkService().create_reset_link(reset_token)

        context = {
            "last_name": user.last_name,
            "first_name": user.first_name,
            "time": datetime.now,
            "reset_link": reset_link,
            "base_ui_url": settings.FRONTEND_HOST_URL,
            "username": user.username,
        }

        body = render_to_string("forgot_password_email.html", context)

        return subject, body, email
