from datetime import datetime

from django.conf import settings
from django.template.loader import render_to_string

from token_management.services.create_reset_token import ResetTokenService
from token_management.services.create_register_token import RegisterTokenService

from user_account.models import User


BASE_MEDIA_HOST = settings.BASE_MEDIA_HOST
BASE_UI_URL = settings.BASE_UI_URL


class EmailPayload:
    @staticmethod
    def reset_password(email: str):
        """
        Activate user email payload.
        """
        user = User.get_user_by_email(email=email)
        subject = "Đặt lại mật khẩu"
        ResetTokenService.deactivate(user)

        reset_token = ResetTokenService().create_reset_token(user=user)

        context = {
            "last_name": user.last_name,
            "first_name": user.first_name,
            "time": datetime.now,
            "reset_link": f"{settings.BASE_UI_URL}/reset-password/{reset_token}",
            "base_ui_url": BASE_UI_URL,
        }

        body = render_to_string("forgot_password_email.html", context)

        return subject, body, email

    @staticmethod
    def verify_email(email: str):
        """
        Activate user email payload.
        """
        user = User.get_user_by_email(email=email)
        subject = "Đăng ký tài khoản"
        RegisterTokenService.deactivate(user)

        context = {
            "last_name": user.last_name,
            "first_name": user.first_name,
            "time": datetime.now,
            "register_token": RegisterTokenService().create_register_token(user=user),
            "base_ui_url": BASE_UI_URL,
        }

        body = render_to_string("register_verify_email.html", context)

        return subject, body, email
